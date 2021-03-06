# 一键爬取链家所有租房信息
## 获取项目
> git clone https://github.com/siskinc/lianjia_spider

## 使用条件
    1. docker
    2. docker-compose
## 使用方法
### 运行爬虫
```
    // 构建spider镜像
    sudo make spider_build //此处需要的时间可能比较长,请耐心等候
    // 运行爬虫
    sudo make up
```

### 查看爬虫日志
```
    sudo docker logs -f lianjia_lianjia_1
```

- 日志结果类似于此
```
--------------------------------------
开始
保存 佛山市 东怡花园 3室2厅 3000元 
保存 广州市 祈福新村山泉居 实用三房 采光好保养新净 
保存 广州市 半岛花园 两房一厅 
保存 廊坊市 鑫乐汇 1室0厅 1400元 
保存 廊坊市 燕京航城 1室1厅 1300元 
保存 廊坊市 东贸国际 1室1厅 2200元 
保存 廊坊市 雷捷小区 3室1厅 1600元 
保存 天津市 五峰里 2室1厅 2000元 
保存 天津市 国耀上河城 3室1厅 2200元 
保存 武汉市 月湖琴声 3室2厅 4500元 
保存 武汉市 保利花园 3室2厅 3500元 
保存 天津市 近园里 3室一厅 距地铁站300米 
保存 天津市 悦府家园两室空房 可长租 办公优质好房 
保存 武汉市 中北路 凯德1818 楚汉汉街地铁站C出口 精装2房 
保存 廊坊市 潮白星光公馆 2室1厅 2400元 
保存 天津市 万科水晶城聆梦园 1室1厅 2700元 
```

## 说明
1. 项目使用Scrapy
2. 该爬虫仅可作为学习使用,若使用于其他用途,请右上角点X
3. 该项目中的MongoDB镜像映射端口默认为27017,Redis默认映射端口为6379,如果跟您本机的MongoDB,Redis或者Docker镜像端口冲突,请自行修改docker-compose.yml文件中mongo与redis的ports属性
4. 爬虫的错误日志在项目中的logs/log文件中,如果没有只能说运行过程中还未报错
5. 该爬虫使用Redis去重