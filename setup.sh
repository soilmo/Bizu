mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
[theme]\n\
primaryColor="#1827E8"\n\
backgroundColor="#02091c"\n\
secondaryBackgroundColor="#586e75"\n\
textColor="#fafafa"\n\
font="sans serif"\n\
\n\
" > ~/.streamlit/config.toml
