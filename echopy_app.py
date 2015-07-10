import ssl 

ssl_enable = True

def run(app):
    try:
        if ssl_enable:
            #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            #context.load_cert_chain('yourserver.crt', 'yourserver.key')
            '''
            Generate a private key:
                openssl genrsa -des3 -out server.key 1024

                Generate a CSR
                openssl req -new -key server.key -out server.csr

                Remove Passphrase from key
                cp server.key server.key.org openssl rsa -in server.key.org -out server.key

                Generate self signed certificate
                openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
            '''

            app.run(debug=True,
                    port=5000,
                    threaded=True,
                    use_reloader=False,
                    use_debugger=True,
                    ssl_context='adhoc', # ssl_context=('yourserver.crt', 'yourserver.key')
                    host='0.0.0.0'
                    )
        else:
            app.run(debug=True,
                port=5000,
                threaded=True,
                use_reloader=False,
                use_debugger=True,
                host='0.0.0.0'
                )
    finally:
        print "Disconnecting clients"

    print "Done"