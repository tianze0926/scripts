fn main() {
    let body = reqwest::blocking::get(
        "http://myhome.tsinghua.edu.cn").unwrap()
    .text().unwrap();

    println!("body = {:?}", body);
}
