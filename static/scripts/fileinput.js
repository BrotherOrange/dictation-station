var myFile = "";

function FileInput(val){
    var file = val.files[0];
    if (!/audio\/\w+/.test(file.type)) {/*可以把autio改成其他文件类型 比如 image*/
        alert("只能选择音频文件");
        return;
    }
    console.log(file.type);/*文件类型*/
    var s = document.getElementById("fileInput").value;
    lst = s.split('\\');
    myFile = lst[lst.length - 1];
    console.log(myFile);
    localStorage.setItem("myFile", myFile);
}

function recognize(val){
    myFile = localStorage.getItem("myFile");
    myLanguage = document.getElementById("select-language").value;
    console.log(myFile);
    var name = {"filename": myFile, "language": myLanguage};

    if (myFile !== "") {
        console.log(myLanguage);
        $.ajax({
            url: '/speech_recognizer',
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            dataType: 'json',
            data: JSON.stringify(name),
            success: function(data) {
            document.getElementById("text-of-voice").textContent = data['text'];
            console.log("Everything has been done");
            localStorage.setItem("myFile", "");
            },
            error: function(){console.log(myFile);}
      })
    }
}

function translation(e){
    var translateVal = document.getElementById("text-of-voice").textContent;
    var languageVal = "zh-Hans";
    var translateRequest = { 'text': translateVal, 'to': languageVal }
  
    if (translateVal !== "") {
      $.ajax({
        url: '/speech_translator',
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(translateRequest),
        success: function(data) {
          for (var i = 0; i < data.length; i++) {
            document.getElementById("translation-of-voice").textContent = data[i].translations[0].text;
            var lang = "";
            if (data[i].detectedLanguage.language === "en"){
                console.log("en");
                lang = "英语";
            }
            else if(data[i].detectedLanguage.language === "de"){
                console.log("de");
                lang = "德语";
            }
            else if(data[i].detectedLanguage.language === "fr"){
                console.log("fr");
                lang = "法语";
            }
            else if(data[i].detectedLanguage.language === "es"){
                console.log("es");
                lang = "西班牙语";
            }
            document.getElementById("detected-language-result").textContent = lang;
            if (document.getElementById("detected-language-result").textContent !== "" && document.getElementById("select-language").value === "auto"){
              document.getElementById("detected-language").style.display = "block";
            }
          }
        }
      });
    };
}

function keyword(e){
    var inputText = document.getElementById("text-of-voice").textContent;
    var inputLanguage = document.getElementById("detected-language-result").textContent;
    if (inputLanguage === "德语"){
        inputLanguage = "de";
    }
    else if (inputLanguage === "英语"){
        inputLanguage = "en";
    }
    else if (inputLanguage === "法语"){
        inputLanguage = "fr";
    }
    else if (inputLanguage === "西班牙语"){
        inputLanguage = "es";
    }

    var sentimentRequest = { "inputText": inputText, "inputLanguage": inputLanguage};

    if (inputText !== "") {
        $.ajax({
            url: '/keywords_extract',
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            dataType: 'json',
            data: JSON.stringify(sentimentRequest),
            success: function(data) {
                for (var i = 0; i < data.documents.length; i++) {
                    if (typeof data.documents[i] !== 'undefined'){
                        if (data.documents[i].id === "1") {
                            document.getElementById("original-keywords").textContent = data.documents[i].keyPhrases;
                            console.log("1");
                        }
                    }
                }
                if (document.getElementById("original-keywords").textContent !== ''){
                    console.log("2");
                    document.getElementById("keywords").style.display = "block";
                }
            }
        });
        console.log("done");
    }
}