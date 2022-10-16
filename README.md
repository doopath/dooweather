# DooWeather

## Preview
**DooWeather** is a crossplatform app written in Python with [Kivymd](https://github.com/kivymd/KivyMD) library.

![no image](https://raw.githubusercontent.com/doopath/dooweather/master/images/dooweather_project_preview.png)

## Navigation
There are some links that help you to navigate README:
* [Preview](https://github.com/doopath/dooweather#preview)
* [Navigation](https://github.com/doopath/dooweather#navigation)
* [Platforms](https://github.com/doopath/dooweather#platforms)
* [Requirements](https://github.com/doopath/dooweather#requirements)
* [Installation](https://github.com/doopath/dooweather#installation)

## Platforms
Supported platforms:
* Linux
* Windows
* OSX
* Android

This project is not depends on a platform so you can build it for anything where Python runs, but officially there is support only for Linux, Windows, OSX and Android.

## Requirements
You need to have python3.9 or newer installed on your machine (only for desktop OS)
If you want to build the app from sources then you need to install _dependencies.txt_:
```bash python -m pip install -r dependencies.txt```

## Installation
There are three prebuilds actually: for Android, Windows and Linux.

### Android
If you want to install **DooWeather** on your Android phone then you need to just downloan .apk file from last [release](https://github.com/doopath/dooweather/releases), find it in your phone's file manager and install.

### Linux and Windows
For Linux or Windows installation you need to download a .whl file from last [release](https://github.com/doopath/dooweather/releases) and install it with _pip install_ command.

Latest release installation sample for Linux:
```bash
wget 'https://github.com/doopath/dooweather/releases/download/1.0/DooWeather-1.0-python3.9.whl'
python -m pip install DooWeather-1.0-python3.9.whl 
```
