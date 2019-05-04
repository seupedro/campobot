#!/usr/bin/env bash
docker run -it --rm \
    --network camponet \
    --name express \
    -p 8081:8081 \
    -e ME_CONFIG_OPTIONS_EDITORTHEME="ambiance" \
    -e ME_CONFIG_MONGODB_SERVER="campodb" \
    -e ME_CONFIG_MONGODB_AUTH_DATABASE="campo" \
    -e ME_CONFIG_MONGODB_ADMINUSERNAME="rootQ4dGr" \
    -e ME_CONFIG_MONGODB_ADMINPASSWORD="bjxTCEuda8b3" \
    mongo-express

#    Name                            | Default         | Description
#    --------------------------------|-----------------|------------
#    ME_CONFIG_BASICAUTH_USERNAME    | ''              | mongo-express web username
#    ME_CONFIG_BASICAUTH_PASSWORD    | ''              | mongo-express web password
#    ME_CONFIG_MONGODB_ENABLE_ADMIN  | 'true'          | Enable admin access to all databases. Send strings: `"true"` or `"false"`
#    ME_CONFIG_MONGODB_ADMINUSERNAME | ''              | MongoDB admin username
#    ME_CONFIG_MONGODB_ADMINPASSWORD | ''              | MongoDB admin password
#    ME_CONFIG_MONGODB_PORT          | 27017           | MongoDB port
#    ME_CONFIG_MONGODB_SERVER        | 'mongo'         | MongoDB container name. Use comma delimited list of host names for replica sets.
#    ME_CONFIG_OPTIONS_EDITORTHEME   | 'default'       | mongo-express editor color theme, [more here](http://codemirror.net/demo/theme.html)
#    ME_CONFIG_REQUEST_SIZE          | '100kb'         | Maximum payload size. CRUD operations above this size will fail in [body-parser](https://www.npmjs.com/package/body-parser).
#    ME_CONFIG_SITE_BASEURL          | '/'             | Set the baseUrl to ease mounting at a subdirectory. Remember to include a leading and trailing slash.
#    ME_CONFIG_SITE_COOKIESECRET     | 'cookiesecret'  | String used by [cookie-parser middleware](https://www.npmjs.com/package/cookie-parser) to sign cookies.
#    ME_CONFIG_SITE_SESSIONSECRET    | 'sessionsecret' | String used to sign the session ID cookie by [express-session middleware](https://www.npmjs.com/package/express-session).
#    ME_CONFIG_SITE_SSL_ENABLED      | 'false'         | Enable SSL.
#    ME_CONFIG_SITE_SSL_CRT_PATH     | ''              | SSL certificate file.
#    ME_CONFIG_SITE_SSL_KEY_PATH     | ''              | SSL key file.

#    Name                            | Default         | Description
#    --------------------------------|-----------------|------------
#    ME_CONFIG_MONGODB_AUTH_DATABASE | 'db'            | Database name
#    ME_CONFIG_MONGODB_AUTH_USERNAME | 'admin'         | Database username
#    ME_CONFIG_MONGODB_AUTH_PASSWORD | 'pass'          | Database password