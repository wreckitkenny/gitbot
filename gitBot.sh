# export PYTHON_HOME=/usr/lib/python3.8
export PYTHON_BINARY=/usr/bin/python3.8
# export PATH=$PYTHON_HOME/python3:$PATH
export GITBOT_HOME=$PWD
export GITBOT_BINARY=gitBot.py

gitBot_pid(){
    echo `ps -ef | grep $GITBOT_BINARY | grep -v grep | awk '{print $2}'`
}

start() {
    pid=$(gitBot_pid)
    if [ -n "$pid" ]; then echo -e "\e[00;31mGITBOT is already running (pid: $pid)\e[00m"
    else 
        echo -e "\e[00;32mStarting GITBOT\e[00m"
        $PYTHON_BINARY $GITBOT_HOME/$GITBOT_BINARY & >> /dev/null
        status
    fi
    return 0
}

status() {
    pid=$(gitBot_pid)
    if [ -n "$pid" ]; then echo -e "\e[00;32mGITBOT is running with pid: $pid\e[00m"
    else 
        echo -e "\e[00;31mGITBOT is not running\e[00m"
        return 3
    fi
}

stop() {
    pid=$(gitBot_pid)
    if [ -n "$pid" ]; then 
        echo -e "\e[00;31mStoping GITBOT\e[00m"
        kill -9 $(gitBot_pid)
    fi
}

case $1 in
    start)
        start
        ;;

    stop)
        stop
        ;;

    restart)
        stop
        start
        ;;

    status)
        status
        exit $?
        ;;

    *)
        echo "Usage: $0 {start|restart|stop|status}"
        ;;
esac
exit 0