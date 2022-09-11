use std::{error::Error, time::Duration, env};
use chrono::Utc;
use lettre::{Message, SmtpTransport, Transport, transport::smtp::authentication::Credentials, message::SinglePart};
use reqwest::{Client, header, Url, StatusCode, redirect};
use scraper::{Html, Selector};
use tokio::time;

struct Checker {
    client_myhome: Client,
    client_payment: Client,
}

impl Checker {
    fn new() -> Self {
        
        Self { 
            client_myhome: {
                let mut headers = header::HeaderMap::new();
                headers.insert(header::ACCEPT, "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8".parse().unwrap());
                headers.insert(header::ACCEPT_ENCODING, "gzip, deflate".parse().unwrap());
                headers.insert(header::ACCEPT_LANGUAGE, "en-US,en;q=0.5".parse().unwrap());
                headers.insert(header::CONNECTION, "keep-alive".parse().unwrap());
                headers.insert(header::DNT, "1".parse().unwrap());
                headers.insert(header::UPGRADE_INSECURE_REQUESTS, "1".parse().unwrap());
                headers.insert(header::USER_AGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0".parse().unwrap());
                Client::builder()
                    .default_headers(headers)
                    .cookie_store(true)
                    .build().unwrap()
            },
            client_payment: {
                let mut headers = header::HeaderMap::new();
                headers.insert(header::USER_AGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0".parse().unwrap());
                Client::builder()
                    .default_headers(headers)
                    .cookie_store(true)
                    .redirect(redirect::Policy::none())
                    .build().unwrap()
            },
        }
    }

    fn value_of_id<'a>(html: &'a Html, id: &'a str) -> Result<(&'a str, &'a str), Box<dyn Error>> {
        let sel = Selector::parse(&format!("#{id}")).unwrap();
        let value = html.select(&sel).next().ok_or("select err")?
            .value().attr("value").ok_or("no value")?;
        Ok((id, value))
    }

    async fn get_avail(&self, username: &str, password: &str) -> Result<u32, Box<dyn Error>> {
        let base = Url::parse("http://myhome.tsinghua.edu.cn").unwrap();
        
        // first page, to acquire cookie ASP.NET_SessionId
        let first_page = self.client_myhome.get(base.as_ref())
            .send().await?
            .text_with_charset("GBK").await?;
        let first_page = Html::parse_document(&first_page);
        
        let form = ["__VIEWSTATE", "__VIEWSTATEGENERATOR"].into_iter()
            .map(|id| Self::value_of_id(&first_page, id)).collect::<Result<Vec<_>, _>>()?.into_iter()
            .chain([
                ("net_Default_LoginCtrl1$txtUserName", username),
                ("net_Default_LoginCtrl1$txtUserPwd", password),
                ("net_Default_LoginCtrl1$lbtnLogin.x", "19"),
                ("net_Default_LoginCtrl1$lbtnLogin.y", "10"),
                ("net_Default_LoginCtrl1$txtSearch1", ""),
                ("Home_Img_NewsCtrl1$hfJsImg", ""),
                ("Home_Img_ActivityCtrl1$hfScript", ""),
            ].into_iter())
            .collect::<Vec<_>>();
        // login
        self.client_myhome.post(base.join("default.aspx").unwrap())
            .form(&form)
            .send().await?;
        
        // lookup available electricity
        let avail_page = self.client_myhome.get(base.join("Netweb_List/Netweb_Home_electricity_Detail.aspx").unwrap())
            .send().await?
            .text_with_charset("GBK").await?;
        let avail_page = Html::parse_document(&avail_page);
        
        let sel = Selector::parse("#Netweb_Home_electricity_DetailCtrl1_lblele").unwrap();
        let e = avail_page.select(&sel).next().ok_or("select err")?;
        let avail = e.text().next().ok_or("no text")?.parse::<u32>()?;
        Ok(avail)
    }

    fn parse_form(page: &str) -> Result<(Vec<(String, String)>, String), Box<dyn Error>> {
        let html = Html::parse_document(page);
        let sel = Selector::parse("input").unwrap();
        let form = html.select(&sel)
            .filter(|e| e.value().attr("name").is_some())
            .map(|e| {
                let name = e.value().attr("name").ok_or("no name")?.to_string();
                let value = e.value().attr("value").ok_or("no value")?.to_string();
                Ok((name, value))
            })
            .collect::<Result<Vec<_>, Box<dyn Error>>>()?;
        let sel = Selector::parse("form").unwrap();
        let next_url = html.select(&sel)
            .next().ok_or("select err")?
            .value().attr("action").ok_or("no action")?
            .to_string();
        Ok((form, next_url))
    }

    async fn get_payment_link(&self, money: u64) -> Result<String, Box<dyn Error>> {
        // GET myhome.tsinghua.edu.cn to acquire __VIEWSTATE, etc
        let myhome_recharge_page = self.client_myhome.get("http://myhome.tsinghua.edu.cn/netweb_user/recharge_ele.aspx")
            .send().await?
            .text_with_charset("GBK").await?;
        let myhome_recharge_page = Html::parse_document(&myhome_recharge_page);
        let money_str = money.to_string();
        let form = ["__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTTARGET", "__EVENTARGUMENT"].into_iter()
            .map(|id| Self::value_of_id(&myhome_recharge_page, id))
            .chain(["username", "louhao", "room", "student_id"].into_iter()
                .map(|name| {
                    let sel = Selector::parse(&format!(r#"input[name="{}"]"#, name)).unwrap();
                    let value = myhome_recharge_page.select(&sel).next().ok_or("select err")?
                        .value().attr("value").ok_or("no value")?;
                    Ok((name, value))
                })
            ).collect::<Result<Vec<_>, _>>()?.into_iter()
            .chain([
                ("recharge_eleCtrl1$RadioButtonList1", "支付宝支付"),
                ("banktype", "alipay"),
                ("write_money", &money_str),
            ].into_iter());
        let urlencoded_form = form_urlencoded::Serializer::new(String::new())
            .encoding_override(Some(&|s| encoding_rs::GBK.encode(s).0))    
            .extend_pairs(form).finish();

        // POST myhome.tsinghua.edu.cn
        let myhome_post_page = self.client_payment.post("http://myhome.tsinghua.edu.cn/netweb_user/recharge_pay_ele.aspx")
            .header(header::CONTENT_TYPE, "application/x-www-form-urlencoded")
            .body(urlencoded_form)
            .send().await?
            .text_with_charset("GBK").await?;
        let (form, next_url) = Self::parse_form(&myhome_post_page)?;
        
        // POST https://fa-online.tsinghua.edu.cn/...
        let faonline_post_page = self.client_payment.post(next_url)
            .form(&form)
            .send().await?
            .text().await?;
        let (form, next_url) = Self::parse_form(&faonline_post_page)?;

        // POST https://openapi.alipay.com/...
        let response = self.client_payment.post(next_url)
            .form(&form)
            .send().await?;
        if response.status() != StatusCode::FOUND {
            return Err("should be 302".into());
        }
        let next_url = response.headers()
            .get(header::LOCATION).ok_or("no location")?
            .to_str()?;

        // GET https://unitradeprod.alipay.com/...
        let response = self.client_payment.get(next_url)
            .send().await?;
        if response.status() != StatusCode::FOUND {
            return Err("should be 302".into());
        }
        let next_url = response.headers()
            .get(header::LOCATION).ok_or("no location")?
            .to_str()?;

        // GET https://excashier.alipay.com/...
        let res = self.client_payment.get(next_url)
            .send().await?
            .text_with_charset("GBK").await?;
        let res = Html::parse_document(&res);
        let sel = Selector::parse("#J_qrCode").unwrap();
        let link = res.select(&sel)
            .next().ok_or("no payment link")?
            .value().attr("value").ok_or("no value")?.to_string();

        Ok(link)
    }
}

fn send_email(from: &str, to: &str, subject: &str, body: String,
    smtp_server: &str, smtp_username: &str, smtp_password: &str, smtp_port: &str
) -> Result<String, Box<dyn Error>>{
    let email = Message::builder()
        .from(from.parse().unwrap())
        .to(to.parse().unwrap())
        .subject(subject)
        .singlepart(SinglePart::html(body))
        .unwrap();
    let mailer = SmtpTransport::relay(smtp_server).unwrap()
        .credentials(Credentials::new(smtp_username.to_string(), smtp_password.to_string()))
        .port(smtp_port.parse().unwrap())
        .build();
    let response = mailer.send(&email)?;
    let message = response.message().collect::<Vec<_>>().join("\n");
    Ok(message)
}

async fn exec() -> Result<(), Box<dyn Error>> {
    let now = Utc::now();
    println!("{}", now);
    
    let checker = Checker::new();

    let avail = checker.get_avail(
        &env::var("MYHOME_USERNAME").unwrap(),
        &env::var("MYHOME_PASSWORD").unwrap(),
    ).await?;

    let threshold = env::var("MYHOME_REMAIN_THRESHOLD").unwrap()
        .parse().unwrap();
    if avail < threshold {
        println!("Remain ({avail}) is below threshold ({threshold})");

        let link = checker.get_payment_link(
            env::var("MYHOME_MONEY").unwrap().parse().unwrap()
        ).await?;
        println!("Payment link: {link}");
        
        let message = send_email(
            &env::var("EMAIL_FROM").unwrap(),
            &env::var("EMAIL_TO").unwrap(),
            &env::var("EMAIL_SUBJECT").unwrap(),
            env::var("EMAIL_BODY").unwrap()
                .replace("{REMAIN}", &avail.to_string())
                .replace("{LINK}", &link),
            &env::var("SMTP_SERVER").unwrap(),
            &env::var("SMTP_USERNAME").unwrap(),
            &env::var("SMTP_PASSWORD").unwrap(),
            &env::var("SMTP_PORT").unwrap(),
        )?;
        println!("Email sent: {}", message);
    } else {
        println!("Remain: {avail}");
    }
    
    Ok(())
}

#[tokio::main]
async fn main() {
    let check_period = env::var("CHECK_PERIOD").unwrap().parse().unwrap();
    let retry_period = env::var("RETRY_PERIOD").unwrap().parse().unwrap();
    let mut interval = time::interval(Duration::from_secs(check_period));
    loop {
        interval.tick().await;
        loop {
            match exec().await {
                Ok(()) => break,
                Err(e) => {
                    time::sleep(Duration::from_secs(retry_period)).await;
                    println!("{:?}", e);
                }
            }
        }
        
    }
}
