# Tsinghua Myhome Electricity Check

Periodically check remaining electricity, and send an email with Alipay payment link when running out.

## Use

Docker Compose:

```yaml
version: '3'

services:
  app:
    image: tz039e/electricity-check
    restart: always
    env_file: .env
```

### Environment Variables

- `MYHOME_USERNAME`: Myhome username
- `MYHOME_PASSWORD`: Myhome password **(not Tsinghua ID password)**
- `MYHOME_REMAIN_THRESHOLD`: would send email when remaining electricity is below this threshold. (unit: kW⋅h)
- `MYHOME_MONEY`: payment amount (unit: CNY)
- `EMAIL_FROM`: name plus address, e.g. `John Smith <example@email.com>`, see [Mailbox in lettre::message](https://docs.rs/lettre/latest/lettre/message/struct.Mailbox.html) for example
- `EMAIL_TO`: name plus address, e.g. `John Smith <example@email.com>`, see [Mailbox in lettre::message](https://docs.rs/lettre/latest/lettre/message/struct.Mailbox.html) for example
- `EMAIL_SUBJECT`
- `EMAIL_BODY`: template of email body in HTML format
  - placeholders:
    - `{REMAIN}`: remaining electricity (unit: kW⋅h)
    - `{LINK}`: payment link
  - example:
    ```
    Electricity is running out: <b>{REMAIN}</b> kW⋅h remained. <br> Open the following link to recharge: {LINK}
    ```
- `SMTP_SERVER`
- `SMTP_USERNAME`
- `SMTP_PASSWORD`
- `SMTP_PORT`
- `CHECK_PERIOD`: query inerval (unit: seconds)
- `RETRY_PERIOD`: period to wait if error occurs  (unit: seconds)

> Note that variables with spaces would need enclosing with apostrophes (`'`) in the `.env` file.
