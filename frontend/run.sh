export PROJECT_BASE_DIR=../
# load api_key from ./api_key.txt if there exists
if [ -f ./api_key.txt ]; then
    export ZHIPUAI_API=$(cat ./api_key.txt)
fi
# run on 8080
streamlit run main.py --server.port 8080