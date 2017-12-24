var devArrayObj = JSON.parse(counts);
// alert(devArrayObj);
function healthcolor(health)
    {
        var health;
        if (health == 4)
        {return "green";}
        else if (health == 3)
        {return "blue";}
        else if (health == 2)
        {return "orange";}
        else if (health == 1)
        {return "red";}
        else
        {return "pink";}
    }

function showmanagecolor()
{
    for(i=0 ; i<devArrayObj.length ; i++)
    {
        devArrayObj[i].devV = healthcolor(devArrayObj[i].devManageGrade);
        var did = document.getElementById(devArrayObj[i].devid);
        if (did){
        did.setAttribute("stroke",devArrayObj[i].devV);
        }
    }
}

function showhealthcolor()
{
    for(i=0 ; i<devArrayObj.length ; i++)
    {
        var devhealth;
        if (devArrayObj[i].devHealth=="严重")
        {
            devhealth=1;
        }
        else if(devArrayObj[i].devHealth=="异常")
        {
            devhealth=2;
        }
        else if(devArrayObj[i].devHealth=="注意")
        {
            devhealth=3;
        }
        else if(devArrayObj[i].devHealth=="正常")
        {
            devhealth=4;
        }
        else{
            alert ("设备健康度定义错误")
        }
        devArrayObj[i].devV = healthcolor(devhealth);
        var did = document.getElementById(devArrayObj[i].devid);
        if (did){
        did.setAttribute("stroke",devArrayObj[i].devV);
        }
    }
}

function showimportancecolor()
{
    for(i=0 ; i<devArrayObj.length ; i++) {
        var devimportance;
        if (devArrayObj[i].devImportance == "关键") {
            devimportance = 1;
        }
        else if (devArrayObj[i].devImportance == "重要") {
            devimportance = 2;
        }
        else if (devArrayObj[i].devImportance == "关注") {
            devimportance = 3;
        }
        else if (devArrayObj[i].devImportance == "一般") {
            devimportance = 4;
        }
        else {
            devimportance = 0;
        }
        devArrayObj[i].devV = healthcolor(devimportance);
        var did = document.getElementById(devArrayObj[i].devid);
        $(did).attr("stroke", devArrayObj[i].devV);

    }
}

for(i=0 ; i<devArrayObj.length ; i++) {
    var did =document.getElementById(devArrayObj[i].devid);
    if (did){
        var title = document.createElementNS("http://www.w3.org/2000/svg","title"),
    msg=devArrayObj[i].devname;
    text = document.createTextNode(msg);
    title.appendChild(text);
    did.appendChild(title);
    }

}
