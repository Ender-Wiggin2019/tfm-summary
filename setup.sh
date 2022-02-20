mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"117010097@link.cuhk.edu.cn\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = 10000\n\
" > ~/.streamlit/config.toml