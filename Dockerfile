FROM centos
MAINTAINER mix

USER root

#base設定
RUN yum -y update && yum -y groupinstall 'Development tools' && \
	yum -y install vim \
	#pyenvに必要
	readline-devel \
	zlib-devel \
	bzip2-devel \
	sqlite-devel \
	openssl-devel \
	#phantomjsに必要
	fontconfig-devel \
#phantomjs用
RUN yum -y install epel-release
RUN rpm -ivh http://repo.okay.com.mx/centos/7/x86_64/release/okay-release-1-1.noarch.rpm
RUN yum -y install phantomjs
#cronのインストール https://www.server-world.info/query?os=CentOS_7&p=initial_conf&f=9
RUN yum -y install cronie-noanacron && yum -y remove cronie-anacron
#locale設定
# 参考 http://qiita.com/suin/items/856bf782d0d295352e51
# 参考 http://qiita.com/yuki2006/items/6cea8c352e38f047b52a#comment-8e863c71962008035d0d
RUN yum -y reinstall glibc-common
RUN localedef -v -c -i ja_JP -f UTF-8 ja_JP.UTF-8; echo "";
env LANG=ja_JP.UTF-8
RUN rm -f /etc/localtime
RUN ln -fs /usr/share/zoneinfo/Asia/Tokyo /etc/localtime

RUN yum clean all

#Pythonのインストール
RUN git clone https://github.com/yyuu/pyenv.git /root/.pyenv
RUN echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
RUN echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
RUN echo 'eval "$(pyenv init -)"' >> ~/.bashrc
#pyenv環境変数
ENV PYENV_ROOT /root/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH
RUN pyenv install 3.6.1

WORKDIR /root/
RUN pyenv local 3.6.1
RUN pip install selenium

#crontabの設定
RUN echo "*/1 * * * * cd /root/app/; /root/.pyenv/shims/python main.py phantomjs" >> /var/spool/cron/root

#nodejsのインストールとphantomjsのインストール
#RUN curl -L git.io/nodebrew | perl - setup
#RUN echo 'export PATH=$HOME/.nodebrew/current/bin:$PATH' >> ~/.bashrc
#ENV NODEBREW_ROOT /root/.nodebrew
#ENV PATH $NODEBREW_ROOT:$PATH
#RUN nodebrew install-binary 7.10.0
#RUN nodebrew use 7.10.0
#
#RUN mkdir ~/.npm-global
#RUN /root/.nodebrew/current/bin/npm config set prefix '~/.npm-global'
#RUN echo 'export PATH="/root/.npm-global/bin:$PATH"' >> ~/.bashrc
#ENV PATH /root/.npm-global/bin:$PATH

#RUN /root/.nodebrew/current/bin/npm install -g phantomjs
#RUN ln -s ~/node_modules/phantomjs/bin/phantomjs /usr/local/bin/
