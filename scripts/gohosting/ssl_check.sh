openssl s_client -connect nisade.com:443 | openssl x509 -noout -dates
echo $DOM:$PORT && echo | openssl s_client -connect ${DOM}:${PORT} -servername ${DOM}  | ^Censsl x509 -noout -dates -text | grep -E '^not|DNS:'
