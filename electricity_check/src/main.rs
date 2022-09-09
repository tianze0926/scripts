use std::time::Duration;

use regex::RegexBuilder;
use reqwest::{Client, header, Url};
use tokio::time;

async fn get_avail() -> Result<u32, Box<dyn std::error::Error>> {
    let mut headers = header::HeaderMap::new();
    headers.insert(header::ACCEPT, "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8".parse().unwrap());
    headers.insert(header::ACCEPT_ENCODING, "gzip, deflate".parse().unwrap());
    headers.insert(header::ACCEPT_LANGUAGE, "en-US,en;q=0.5".parse().unwrap());
    headers.insert(header::CONNECTION, "keep-alive".parse().unwrap());
    headers.insert(header::DNT, "1".parse().unwrap());
    headers.insert(header::UPGRADE_INSECURE_REQUESTS, "1".parse().unwrap());
    headers.insert(header::USER_AGENT, "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0".parse().unwrap());

    let base = Url::parse("http://myhome.tsinghua.edu.cn").unwrap();
    let client = Client::builder()
        .default_headers(headers)
        .cookie_store(true)
        .build()?;
    
    // first page, to acquire cookie ASP.NET_SessionId
    let first_page = client.get(base.as_ref())
        .send().await?
        .text_with_charset("GBK").await?;
    
    // get certain fields as part of the later login post form
    let extractor = |id: &str| -> Result<&str, Box<dyn std::error::Error>> {
        let re = RegexBuilder::new(
                &format!(r#"<input.*id="{}".*value="(.*)" />"#, id)
            ).swap_greed(true).build()?;
        let value = re
            .captures(&first_page).ok_or(format!("{} no match", id))?
            .get(1).ok_or(format!("{} re group err", id))?
            .as_str();
        Ok(value)
    };
    let viewstate = extractor("__VIEWSTATE")?;
    let viewstategenerator = extractor("__VIEWSTATEGENERATOR")?;

    // login
    client.post(base.join("default.aspx").unwrap())
        .form(&[
            ("__VIEWSTATE", viewstate),
            ("__VIEWSTATEGENERATOR", viewstategenerator),
            ("net_Default_LoginCtrl1$txtUserName", "zhoutz19"),
            ("net_Default_LoginCtrl1$txtUserPwd", "Y281avckhHE0dSCCIHX5"),
            ("net_Default_LoginCtrl1$lbtnLogin.x", "19"),
            ("net_Default_LoginCtrl1$lbtnLogin.y", "10"),
            ("net_Default_LoginCtrl1$txtSearch1", ""),
            ("Home_Img_NewsCtrl1$hfJsImg", ""),
            ("Home_Img_ActivityCtrl1$hfScript", ""),
        ])
        .send().await?;
    
    // lookup available electricity
    let avail_page = client.get(base.join("Netweb_List/Netweb_Home_electricity_Detail.aspx").unwrap())
        .send().await?
        .text_with_charset("GBK").await?;
    let avail: u32 = ({
        let id = "Netweb_Home_electricity_DetailCtrl1_lblele";
        let re = RegexBuilder::new(
            &format!(r#"<span.*id="{}".*>(.*)</span>"#, id)
        ).swap_greed(true).build()?;
        let value = re
            .captures(&avail_page).ok_or(format!("{} no match", id))?
            .get(1).ok_or(format!("{} re group err", id))?
            .as_str();
        Ok(value)
    } as Result<&str, Box<dyn std::error::Error>>)?.parse()?;
    
    Ok(avail)
}


#[tokio::main]
async fn main() {
    let mut interval = time::interval(Duration::from_secs(3600));
    loop {
        interval.tick().await;
        let avail = get_avail().await.unwrap();
        println!("{}", avail);
    }
}
