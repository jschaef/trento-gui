# trento-gui

A web interface for displaying textual output generated using https://github.com/scmschmidt/trento_checks_for_supportconfig.

## requirements

* os: linux
* python3 >= 3.11
* streamlit >= 1.30 (https://streamlit.io/)

## build

```
git clone https://github.com/jschaef/trento-gui.git
cd trento-gui
python3.xx -m venv venv, e.g. python3.11 -m venv venv
source ./venv/bin/activate
pip install -U pip
pip install -r requirement.txt
```

## configure

* edit <code>config.py</code>
* optional:
     edit <code>.streamlit/config.toml</code>

## run


* <code>cd trento-gui</code>
* <code>streamlit run app.py</code>

## access

* open a webbrowser and navigate to the page displayed before
* signup

## usage

* upload a SUSE supportconfig generated on a SAP system
* run a check

## run app behind nginx

```txt
server {
    listen              443 ssl;
    server_name         <fqdn of your server>;
    ssl_certificate     /etc/ssl/server/<pub_cert>.crt.pem;
    ssl_certificate_key /etc/ssl/private/<priv_key>.key.pem;
    
    location / {
            client_max_body_size 2048M;
            proxy_pass http://127.0.0.1:8501;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_read_timeout 86400;
    }
}
```
