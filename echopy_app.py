import ssl 

ssl_enable = False

def run(app):
    try:
        if ssl_enable:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain('yourserver.crt', 'yourserver.key')
            app.run(debug=True,
                    port=5000,
                    threaded=True,
                    use_reloader=False,
                    use_debugger=True,
                    ssl_context=context,
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