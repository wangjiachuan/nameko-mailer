# Mailer services based on Nameko microservices framework

## Dev environment setup (Mac)
 
Ideally you should be working in isolated python virtual environment. 

Clone this report and initialise new virtualenv in the root of the project. 

```sh
$ virtualenv env
```

Activate it:

```sh
$ source env/bin/activate
```

Make sure RabbitMQ is installed and broker is running. 
Despite Nameko instructions broker needs to be started after brew installation on Mac.

```sh
$ brew update
$ brew install rabbitmq
```

In separate terminal session start RabbitMQ broker

```sh
$ /usr/local/sbin/rabbitmq-server
```

Back on our python terminal session install dependencies 

```sh
$ pip install -r requirements.txt
```

Test connectivity between Nameko and RabbitMQ

```sh
$ nameko shell
```

You should see

```sh
Nameko Python 2.7.6 (default, Sep  9 2014, 15:04:36)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] shell on darwin
Broker: amqp://guest:guest@localhost
>>>
```

Type ```exit()``` to stop Nameko interactive session.