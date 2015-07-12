FROM ubuntu:12.04
MAINTAINER adaml, adaml@gigaspaces.com

# update and install dependencies
RUN apt-get -y update && \
    apt-get install -y python-software-properties && \
    add-apt-repository -y ppa:git-core/ppa && \
    apt-get install -y curl wget sudo python-dev bzip2 ruby rpm git make gcc libyaml-dev

# install ruby
RUN /bin/bash -c 'wget https://ftp.ruby-lang.org/pub/ruby/ruby-1.9.3-rc1.tar.bz2 --no-check-certificate && \
	tar -xjf ruby-1.9.3-rc1.tar.bz2 && \
	cd ruby-1.9.3-rc1 && \
	./configure --disable-install-doc && \
	make && \
	make install && \
	cd ~'

# install fpm and configure gem/bundler
RUN gem install fpm --no-ri --no-rdoc && \
	echo -e 'gem: --no-ri --no-rdoc\ninstall: --no-rdoc --no-ri\nupdate:  --no-rdoc --no-ri' >> ~/.gemrc

# install pip
RUN curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python

# install virtualenv
RUN pip install virtualenv==1.11.4
