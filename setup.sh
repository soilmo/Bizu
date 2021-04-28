mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = ""\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor = ‘#84a3a7’\n\
backgroundColor = ‘#EFEDE8’\n\
secondaryBackgroundColor = ‘#fafafa’\n\
textColor= ‘#424242’\n\
font = ‘sans serif’\n\
" > ~/.streamlit/config.toml
