# heroku为php添加拓展

1.在composer.json里边添加拓展

```
{
    "require": {
        "ext-bcmath": "*",
        "ext-mcrypt": "*",
        "ext-memcached": "*",
        "ext-mongodb": "^1.1.0"
    }
}
```

2.更新composer

```
commposer update
```

如何本地没有安装拓展的话，会报错。可以使用以下的方式更新

```
composer update --ignore-platform-reqs
```

参考

https://devcenter.heroku.com/articles/php-support