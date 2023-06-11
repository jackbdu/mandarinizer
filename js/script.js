var chars = findGetParameter("chars");
var res   = findGetParameter("res");         // number of characters of the shorter side
var scl   = findGetParameter("scl");         // scl for exported image
var clr   = findGetParameter("clr");
var wm    = findGetParameter("wm");
var rt    = findGetParameter("rt"); // ratio
var pc    = findGetParameter("pc"); // percentage
var zm    = findGetParameter("zm"); // zoom
var mr    = findGetParameter("mr"); // mirror
var iv    = findGetParameter("iv"); // invert
var rf    = findGetParameter("rf"); // auto refresh
var rft   = findGetParameter("rft"); // auto refresh time
var dev   = findGetParameter("dev"); // device id
chars = chars ? _half2full(chars, {punctuation: true, smart_mode: false}) : "數字未來数字未来ＤＦ";
res   = res ? res : 48;
scl   = scl ? scl : 2;
clr   = clr ? clr : 0;
dev   = dev ? dev : 0;
pc    = pc ? pc : 90;
wm    = wm ? wm : 0;
var videoHeight = res;// by default, landscape, shorter side is height
var ratio = rt ? rt : 4/3;      // width - height ratio
var zoom = zm ? zm : 0;         // value indicating zoom
var charValuePairs = [];
var watermark24 = "富强民主文明和谐自由平等公正法制爱国敬业诚信友善";
var watermark32 = "富强民主文明和谐    自由平等公正法制    爱国敬业诚信友善";
var watermark48 = "富强  民主  文明  和谐   自由  平等  公正  法制   爱国  敬业  诚信  友善";
var watermark64 = "富强  民主  文明  和谐           自由  平等  公正  法制           爱国  敬业  诚信  友善";
var watermark96 = "富 强    民 主    文 明    和 谐            自 由    平 等    公 正    法 制            爱 国    敬 业    诚 信    友 善";
var watermark128 = "富  强      民  主      文  明      和  谐             自  由      平  等      公  正      法  制             爱  国      敬  业      诚  信      友  善";
var watermark = watermark24;  // watermark in use
var infoInfo = "<p style='text-align: left;'>Mandarinizer, developed by <a target='_blank' href='http://jackbdu.com/about'>Jack B. Du</a>, is a camera with Chinese characteristics.</p><br><p style='text-align: left;'>Take pictures by taking screenshots and record videos by recording screen.</p>";
var editInfo = "<input id='chars' type='text' placeholder='Enter characters here...' onkeyup='handleReturnKey();'></input>"

var devicesArray = [];   // array of devices
var deviceIdx = dev;    // index of deviceId in use
var infoCount = 0;

var isWatermarked = (wm == 1);
var isMirrored    = (mr == 1); // whether or not the stream is mirrored
var isActivated   = false; // whether or not the toolbar is activated
var isInverted    = (iv == 1); // whether or not the stream is inverted
var infoIsShown   = false;
var editIsShown   = false;
var isTimeless    = false; // whether or not the time is sepcified
var isColored     = (clr != 0);  // wehther or not the characters are colored

// html elements
var body          = document.body;
var canvas        = document.getElementById("myCanvas");
var myVideo       = document.getElementById('myVideo');
var viewfinder    = document.getElementById("viewfinder");
var credits       = document.getElementById("credits");
var toolbar       = document.getElementById("toolbar");
var copyButton    = document.getElementById("copyButton");
var infoButton    = document.getElementById("infoButton");
var editButton    = document.getElementById("editButton");
var cameraButton  = document.getElementById("cameraButton");
var zoomSlider    = document.getElementById("zoomSlider");
var infoBox       = document.getElementById("infoBox");
var styleTag      = document.getElementsByTagName('style')[0];
var context       = canvas.getContext('2d');

body.style.backgroundColor = isInverted ? "#000" : "#fff";
viewfinder.style.color = isInverted ? "#fff" : "#000";

sortCharsByAlpha(chars);

onResize();

// event listeners
DetectRTC.load(function() {
  if (!DetectRTC.isWebRTCSupported) {
    if (DetectRTC.isMobileDevice) {
      if (DetectRTC.osName == "iOS") {
        if (parseInt(DetectRTC.osVersion.split(".")[0]) < 11) { // iOS needs to be 11+
          displayInfo("Sorry, your current version of iOS doesn't support Mandarinizer. Please update your iOS to the latest version.");
        } else {
          displayInfo("Sorry, this broswer doesn't support Mandarinizer. Please open this page in Safari.");
        }
      } else {
        displayInfo(DetectRTC.osName);
      }
    } else {
      // for non-mobile
      displayInfo("Please open this page with Chrome, Firefox, or Safari.");
    }
  //} else {
  //  infoBox.innerHTML = 'Please allow access to cameras in order to use Mandarinizer.';
  }
});

// copy to clipboard setup
var clipboard = new Clipboard('#copyButton');

clipboard.on('success', function(e) {
    displayInfo("Copied to clipboard", 1500);
    e.clearSelection();
});

clipboard.on('error', function(e) {
    displayInfo("Failed to copy", 1500);
});

zoomSlider.oninput = function() {
  zoom = parseInt(this.value);
  displayInfo(Math.floor(10*(zoom+24)/24)/10+"x", 500);
}

function toggleToolbar() {
  if (infoBox.style.opacity != 0) {
    hideInfo();
    return;
  }
  if (isActivated) {
    copyButton.className = "";
    infoButton.className = "";
    editButton.className = "";
    toolbar.className.includes("landscape") ? toolbar.className = "landscape" : toolbar.className = "";
  } else {
    editButton.className = "activated";
    copyButton.className = "activated";
    infoButton.className = "activated";
    toolbar.className.includes("landscape") ? toolbar.className = "activated landscape" : toolbar.className = "activated";
  }
  isActivated = !isActivated;
}

function toggleInfo() {
  if (infoIsShown) {
    hideInfo();
  } else {
    displayInfo(infoInfo);
    infoIsShown = true;
  }
}

function toggleEdit() {
  if (editIsShown) {
    if (document.getElementById("chars").value) {
      window.location.search = "chars="+document.getElementById("chars").value;
    } else {
      hideInfo();
    }
  } else {
    displayInfo(editInfo);
    editButton.className = 'activated editing';
    document.getElementById("chars").select();
    editIsShown = true;
  }
}

function switchTheme() {
  if(!isColored && !isInverted) {
    isColored = true;
    displayInfo("Bright color mode", 1500);
  } else if (isColored && !isInverted) {
    isInverted = true;
    isColored = false;
    body.style.backgroundColor = "#000";
    viewfinder.style.color = "#fff";
    displayInfo("Dark B & W mode", 1500);
  } else if (!isColored && isInverted) {
    isColored = true;
    displayInfo("Dark color mode", 1500);
  } else if (isColored && isInverted) {
    isColored = false;
    isInverted = false;
    body.style.backgroundColor = "#fff";
    viewfinder.style.color = "#000";
    displayInfo("Bright B & W mode", 1500);
  }
}

function changeRes() {
  if (res < 96) {
    res *= 2;
  } else {
    res = 24;
  }
  videoHeight = res;
  onResize();
  displayInfo(videoHeight*ratio+" x "+videoHeight, 1500);
}

function takePicture() {
  var innerWidth = window.innerWidth;
  var innerHeight = window.innerHeight;
  var picWidth;
  var picHeight;
  var multiple = res/24;
  if (ratio > 1) {
    picWidth = 350*multiple;
    picHeight = 270*multiple;
  } else {
    picWidth = 270*multiple;
    picHeight = 350*multiple;
  }
  html2canvas(document.getElementById("viewfinder"), {
    backgroundColor: document.body.style.backgroundColor,
  //  logging: false,
    onclone: oncloneFunction,
//    removeContainer: false,
    scale: scl,
    width: picWidth,
    height: picHeight,
    x: (innerWidth-picWidth)/2,
    y: (innerHeight-picHeight)/2-4*multiple,
  }).then(function(canvas) {
    infoBox.innerHTML = "";
    displayInfo("<img style='width: 100%; border-radius: 0.5em;' src='"+canvas.toDataURL("image/png")+"' />");

    // update the device ids, because somehow device ids are altered after html2canvas
    navigator.mediaDevices.enumerateDevices()
    .then(function(devices) {
      devicesArray = [];   // array of devices
      devices.forEach(function(device) {
        // saves videoinput deviceId in the array
        if (device.kind == "videoinput") {
          devicesArray.push(device);
        }
      });
    })
    .catch(function(err) {
      displayInfo(err.name);
    });

  });
}

function oncloneFunction(doc) {
  var creditsElement = doc.getElementById('credits');
  var pElement = doc.querySelector("#credits > p");
  pElement.style.fontSize = res/24*8+"px";
  pElement.style.height = res/24*8+"px";
  pElement.style.lineHeight = res/24*12+"px";
  doc.getElementById("viewfinder").appendChild(creditsElement);
  doc.getElementById("viewfinder").className = "rendered";
}

function toggleMirror() {
  isMirrored = !isMirrored;
  isMirrored ? displayInfo("Mirror: ON", 1500) : displayInfo("Mirror: OFF", 1500);
}

function switchCamera() {
  if (devicesArray.length > 1) {
    deviceIdx = (deviceIdx+1<devicesArray.length)? deviceIdx + 1 : 0;
    var constraints = {
      audio: false,
      video: {
        deviceId: {exact: devicesArray[deviceIdx].deviceId}
      }
    };
    navigator.mediaDevices.getUserMedia(constraints)
    .then(function success(stream) {
      myVideo.srcObject.getTracks().forEach(function(track) {
        track.stop();
      });
      var deviceLabel = devicesArray[deviceIdx].label.toLowerCase();
      if (deviceLabel.includes('front') || deviceLabel.includes('facetime')) {
        isMirrored = true;
      } else {
        isMirrored = false;
      }

      myVideo.srcObject = stream;
      displayInfo("Camera switched", 1500);
    })
    .catch(function(err) {
      displayInfo(err.name);
    });
  } else {
    displayInfo("No more camera found", 1500);
  }
}



// get the device ids
navigator.mediaDevices.enumerateDevices()
.then(function(devices) {
  devices.forEach(function(device) {
    // saves videoinput deviceId in the array
    if (device.kind == "videoinput") {
      devicesArray.push(device);
    }
  });
  // if videoinput device found
  if (devicesArray.length > 0) {
    if (deviceIdx >= devicesArray.length) {
      deviceIdx = devicesArray.length-1;
    }
    // set up the constraints to use the deviceIdx
    var constraints = {
      audio: false,
      video: {
        deviceId: {exact: devicesArray[deviceIdx].deviceId}
      }
    };
    if (rf == 1) {
      constraints = {
        audio: false,
        video: {
          deviceId: {exact: devicesArray[deviceIdx].deviceId},
          aspectRatio: ratio
        }
      };
    }
    // start up the stream
    navigator.mediaDevices.getUserMedia(constraints)
    .then(function success(stream) {
      // this is after permission is granted, update the device ids
      navigator.mediaDevices.enumerateDevices()
      .then(function(devices) {
        devicesArray = [];   // array of devices
        devices.forEach(function(device) {
          // saves videoinput deviceId in the array
          if (device.kind == "videoinput") {
            devicesArray.push(device);
          }
        });
        if (deviceIdx >= devicesArray.length) {
          deviceIdx = devicesArray.length-1;
        }
        var constraints = {
          audio: false,
          video: {
            deviceId: {exact: devicesArray[deviceIdx].deviceId}
          }
        };
        if (rf == 1) {
          constraints = {
            audio: false,
            video: {
              deviceId: {exact: devicesArray[deviceIdx].deviceId},
              aspectRatio: ratio
            }
          };
        }
        myVideo.setAttribute('autoplay', '');
        myVideo.setAttribute('muted', '');
        myVideo.setAttribute('playsinline', '');
        myVideo.srcObject = stream;
        hideInfo();

        var deviceLabel = devicesArray[deviceIdx].label.toLowerCase();
        if (deviceLabel.includes('front') || deviceLabel.includes('facetime')) {
          isMirrored = true;
        }

        update();
      })
      .catch(function(err) {
        displayInfo(err.name);
      });
    })
    .catch(function(err) {
      displayInfo("Please refresh the page and allow access to the camera in order to use Mandarinizer");
    });
  } else {
    displayInfo("No camera found");
  }
})
.catch(function(err) {
  displayInfo(err.name);
});

function update() {
  var tempZoom = zoom*res/24;
  var frame = [];
  canvas.width = videoHeight*ratio;
  canvas.height = videoHeight;
  context.drawImage(myVideo, -tempZoom*ratio/2, -tempZoom/2, canvas.width+tempZoom*ratio, canvas.height+tempZoom);
  var src = context.getImageData(0, 0, canvas.width, canvas.height).data;
  var range = charValuePairs[charValuePairs.length-1][0];

  for (var i = 0; i < src.length; i += 4) {
    // from https://jsperf.com/convert-rgba-to-grayscale
    var pixel = (src[i] * 306 + src[i + 1] * 601 + src[i + 2] * 117) >> 10;
    if (!isInverted) {
      pixel = 255-pixel;
    }
    if (pixel <= charValuePairs[0][0]/range*255) {
      if (isColored) {
        frame.push("<span style='color:rgb("+src[i]+","+src[i+1]+","+src[i+2]+")'>"+charValuePairs[0][1]+"</span>");
      } else {
        frame.push(charValuePairs[0][1]);
      }
    } else {
      for (var j = 1; j < charValuePairs.length; j++) {
        if (pixel <= charValuePairs[j][0]/range*255 && pixel > charValuePairs[j-1][0]/range*255) {
          if (isColored) {
            frame.push("<span style='color:rgb("+src[i]+","+src[i+1]+","+src[i+2]+")'>"+charValuePairs[j][1]+"</span>");
          } else {
            frame.push(charValuePairs[j][1]);
          }
          break;
        }
      }
    }
  }
  while (viewfinder.firstChild) {
    viewfinder.removeChild(viewfinder.firstChild);
  }
  for (var r = 0; r < canvas.height; r++) {
    var lineOfString = [];
    for (var c = 0; c < canvas.width; c++) {
      lineOfString.push(frame[r*canvas.width+c]);
    }
    if (isMirrored) {
      lineOfString = lineOfString.reverse();
    }
    if (isWatermarked) {
      if (watermark.length > r && watermark.charAt(r) != " ") {
        if (isColored) {
          lineOfString[0] = lineOfString[0].substring(0, lineOfString[0].length - 8) + watermark.charAt(r) + "</span>";
          lineOfString[lineOfString.length-1] = lineOfString[lineOfString.length-1].substring(0, lineOfString[lineOfString.length-1].length - 8) + watermark.charAt(r) + "</span>";
        } else {
          lineOfString[0] = watermark.charAt(r);
          lineOfString[lineOfString.length-1] = watermark.charAt(r);
        }
      }
    }
    var line = document.createElement('p');
    line.innerHTML = lineOfString.join('');
    viewfinder.appendChild(line);
  }
  requestAnimationFrame(update);
}

function onResize() {
  if (window.orientation != undefined) {
    readDeviceOrientation();
  }
  if (isWatermarked) {
    handleWatermark();
  }

  var innerWidth = window.innerWidth;
  var innerHeight = window.innerHeight;
  var thePercentage;
  var theUnit;
  if (innerWidth > innerHeight * ratio) {
    if (ratio > 1) {
      thePercentage = pc;
      theUnit = "vh";
    } else {
      thePercentage = pc/ratio;
      theUnit = "vh";
    }
    toolbar.className.includes("activated") ? toolbar.className = "activated landscape" : toolbar.className = "landscape";
    toolbar.style.top = "50%";
    toolbar.style.right = "-50vh";
    toolbar.style.width = "100vh";
    infoButton.style.top = "auto";
    infoButton.style.right = "auto";
    infoButton.style.bottom = "0.2em";
    infoButton.style.left = "0.2em";
    editButton.style.top = "50%";
    editButton.style.right = "auto";
    editButton.style.bottom = "auto";
    editButton.style.left = "0.2em";
    editButton.style.transform = "translate(0, -50%)";
    copyButton.style.top = "0.2em";
    copyButton.style.right = "auto";
    copyButton.style.bottom = "auto";
    copyButton.style.left = "0.2em";
  } else {
    if (ratio > 1) {
      thePercentage = pc/ratio;
      theUnit = "vw";
    } else {
      thePercentage = pc;
      theUnit = "vw";
    }
    toolbar.className.includes("activated") ? toolbar.className = "activated" : toolbar.className = "";
    toolbar.style.top = "auto";
    toolbar.style.right = "auto";
    toolbar.style.width = "100%";
    infoButton.style.top = "0.2em";
    infoButton.style.right = "auto";
    infoButton.style.bottom = "auto";
    infoButton.style.left = "0.2em";
    editButton.style.top = "0.2em";
    editButton.style.right = "auto";
    editButton.style.bottom = "auto";
    editButton.style.left = "50%";
    editButton.style.transform = "translate(-50%, 0)";
    copyButton.style.top = "0.2em";
    copyButton.style.right = "0.2em";
    copyButton.style.bottom = "auto";
    copyButton.style.left = "auto";
  }
  viewfinder.style.fontSize = thePercentage/res+theUnit;
  styleTag.innerHTML="#viewfinder p {height: "+thePercentage/res+theUnit+";}";
}

function handleWatermark() {
  if (videoHeight >= 128) {
    watermark = watermark128;
  } else if (videoHeight >= 96) {
    watermark = watermark96;
  } else if (videoHeight >= 64) {
    watermark = watermark64;
  } else if (videoHeight >= 48) {
    watermark = watermark48;
  } else if (videoHeight >= 32) {
    watermark = watermark32;
  } else {
    watermark = watermark24;
  }
}

function readDeviceOrientation() {
  if (Math.abs(window.orientation) === 90) {
    // Landscape
    ratio = 4/3;
    videoHeight = res;
  } else {
    // Portrait
    ratio = 3/4;
    videoHeight = res/ratio;
  }
  myVideo.setAttribute('width', videoHeight*ratio);
  myVideo.setAttribute('height', videoHeight);
}

function displayInfo(msg, time=null) {
  infoIsShown = false;
  editIsShown = false;
  editButton.className.includes("activated") ? editButton.className = "activated" : editButton.className = "";
  infoBox.innerHTML = msg;
  infoBox.style.opacity = 1;
  infoBox.style.zIndex = "200";
  if (time!=null) {
    isTimeless = false;
    infoCount++;
    setTimeout(function(){
      if (--infoCount <= 0 && !isTimeless) {
        hideInfo();
      }
    }, time);
  } else {
    isTimeless = true;
  }
}

function hideInfo() {
  infoBox.style.opacity = 0;
  infoBox.style.zIndex = "49";
  infoIsShown = false;
  editIsShown = false;
  editButton.className.includes("activated") ? editButton.className = "activated" : editButton.className = "";
}

function sortCharsByAlpha(text) {
  var tempCanvas = document.createElement('canvas');
  var tempContext = tempCanvas.getContext('2d');
  tempCanvas.width = 20;
  tempCanvas.height = 20;

  for (var i = 0; i < text.length; i++) {
    tempContext.clearRect(0,0,tempCanvas.width,tempCanvas.height);
    var value = 0;
    tempContext.fillText(text.charAt(i), 0, 10);
    tempContext.font = "10px Courier";
    for (var x = 0; x < 12; x++) {
      for (var y = 0; y < 12; y++) {
        value += tempContext.getImageData(x,y,1,1).data[3];
      }
    }
    charValuePairs.push([value, text.charAt(i)]);
  }

  charValuePairs.sort(compareCharValuePair);

  function compareCharValuePair(a, b) {
    return a[0] - b[0];
  }
}

// get parameter by name
// https://stackoverflow.com/questions/5448545/how-to-retrieve-get-parameters-from-javascript
function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    var items = location.search.substr(1).split("&");
    for (var index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    }
    return result;
}

function handleReturnKey() {
  if (event.keyCode == 13) {
    document.getElementById("editButton").click();
  }
}

if (rf == 1) {
  setTimeout(refreshPage, rft ? rft : 1800000);
} else { // display toolbar when not rf is off (not in exhibt mode)
  toggleToolbar();
}

function refreshPage() {
  location.reload();
}
