[app]

title = TotalMess
package.name = totalmess
package.domain = gsog.totalmess

source.dir = ./src
source.include_exts = py,png,jpg,kv,atlas

icon.filename = ./assets/temp.png

version = 0.1
requirements = python3==3.10.11,kivy==2.3.1,git+https://gitlab.com/kivymd/KivyMD.git,Kivy-Garden==0.1.5,kivy-garden.matplotlib==0.1.1.dev0,bleak==0.22.3,setuptools==76.0.0,culsans==0.8.0

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
