功能说明：1、通过https://vps789.com/vps/sum/cfIpTop20接口获取优选ip

2、将优选ip自动添加到cf的域名记录中

3、cf邮箱、globalkey、zoneid、ip需要添加的具体域名需要配置在环境变量中，secret key分别是：EMAIL、GLOBAL_KEY、ZONE_ID、DOMAIN

使用说明：fork此仓库，在Setting --Secrets and Variables中依次添加自己CF的EMAIL、GLOBAL_KEY、ZONE_ID、DOMAIN值即可。每天凌晨1点自动更新，或者手动点击star也能更新。
