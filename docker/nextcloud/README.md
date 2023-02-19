## Reverse Proxy

`config/www/nextcloud/config/config.php`:

```php
$CONFIG = array (
  'overwrite.cli.url' => 'https://cloud.tianze.me:1111',
  'overwritehost' => 'cloud.tianze.me:1111',
  'trusted_proxies' => array (
    0 => '192.168.32.1/20',
  ),
);
```

`config/nginx/site-confs/default.conf`: add the following in the `location ~ \.php(?:$|/)` section:

```
fastcgi_read_timeout 600;
fastcgi_send_timeout 600;
fastcgi_connect_timeout 600;
proxy_connect_timeout 600;
proxy_send_timeout 600;
proxy_read_timeout 600;
send_timeout 600;
```

Change `listen [::]:443 ssl http2 default_server;` at `config/nginx/site-confs/default.conf` to `listen 443 default_server;` to disable SSL. Also disabling gzip can reduce CPU usage.


## OIDC

`config/www/nextcloud/config/config.php`:

```php
$CONFIG = array (
  'oidc_login_provider_url' => 'https://auth.tianze.me:1111',
  'oidc_login_client_id' => 'nextcloud',
  'oidc_login_client_secret' => '4E9DotcCpM5iJPdw43TsSPzRodQGi1Pu9prbaMXAy5T1vE7c1J47vMxa2QaTl9a0g4oq574Y',
  'oidc_login_auto_redirect' => false,
  'oidc_login_end_session_redirect' => false,
  'oidc_login_button_text' => 'Log in with Authelia',
  'oidc_login_hide_password_form' => false,
  'oidc_login_use_id_token' => true,
  'oidc_login_attributes' => array (
    'id' => 'preferred_username',
    'name' => 'name',
    'mail' => 'email',
    'groups' => 'groups',
  ),
  'oidc_login_default_group' => 'oidc',
  'oidc_login_use_external_storage' => false,
  'oidc_login_scope' => 'openid profile email groups',
  'oidc_login_proxy_ldap' => false,
  'oidc_login_disable_registration' => false,
  'oidc_login_redir_fallback' => false,
  'oidc_login_alt_login_page' => 'assets/login.php',
  'oidc_login_tls_verify' => true,
  'oidc_create_groups' => false,
  'oidc_login_webdav_enabled' => false,
  'oidc_login_password_authentication' => false,
  'oidc_login_public_key_caching_time' => 86400,
  'oidc_login_min_time_between_jwks_requests' => 10,
  'oidc_login_well_known_caching_time' => 86400,
  'oidc_login_update_avatar' => false,
);
```