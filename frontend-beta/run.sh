export PROJECT_BASE_DIR=$(dirname $(pwd))
# set pics caching path
export PIC_CACHE_PATH=$PROJECT_BASE_DIR/pics
export OBJ_CACHE_PATH=$PROJECT_BASE_DIR/objs
# set TripoSR project path
export TRIPOSR_HOME=$(dirname $PROJECT_BASE_DIR)/TripoSR

# set huggingface home
export HF_HOME="/hy-tmp/huggingface"    # on gpushare cloud

# load api_key from ./api_key.txt if there exists
if [ -f ./api_key.txt ]; then
    export ZHIPUAI_API=$(cat ./api_key.txt)
fi

# check PROJECT_BASE_DIR
echo "PROJECT_BASE_DIR: $PROJECT_BASE_DIR"
# check PIC_CACHE_PATH
echo "PIC_CACHE_PATH: $PIC_CACHE_PATH"
# check TRIPOSR_HOME
echo "TRIPOSR_HOME: $TRIPOSR_HOME"

# run on 8080
# streamlit run main.py --server.port 8080
streamlit run main.py --server.port 8080
