var $canvas = $('#wc_canvas');
var maskCanvas;

function draw_word_cloud(arr_new){
    //console.log(arr_new)
    width_wc=$('#wordcloud_chart').width()
    height_wc=$('#wordcloud_chart').height()
    makeCanvas(width_wc,height_wc,arr_new)

}

function run(width_wc,height_wc,arr_new) {
    //alert('inside run')

    var width = width_wc;
    var height = height_wc;
    var pixelWidth = width;
    var pixelHeight = height;
    $canvas.css({'width': '', 'height': '' });
    $canvas.attr('width', pixelWidth);
    $canvas.attr('height', pixelHeight);

    if (maskCanvas) {
      
      var bctx = document.createElement('canvas').getContext('2d');
      bctx.fillStyle = '#fff';
      bctx.fillRect(0, 0, 1, 1);
      var bgPixel = bctx.getImageData(0, 0, 1, 1).data;

      var maskCanvasScaled = document.createElement('canvas');
      maskCanvasScaled.width = 600;
      maskCanvasScaled.height = 600;
      var ctx = maskCanvasScaled.getContext('2d');
    
      ctx.drawImage(maskCanvas,
        0, 0, maskCanvas.width, maskCanvas.height,
        0, 0, maskCanvasScaled.width, maskCanvasScaled.height);

      var imageData = ctx.getImageData(0, 0, width, height);
      var newImageData = ctx.createImageData(imageData);
      for (var i = 0; i < imageData.data.length; i += 4) {
        if (imageData.data[i + 3] > 128) {
          newImageData.data[i] = bgPixel[0];
          newImageData.data[i + 1] = bgPixel[1];
          newImageData.data[i + 2] = bgPixel[2];
          newImageData.data[i + 3] = bgPixel[3];
        } else {
          // This color must not be the same w/ the bgPixel.
          newImageData.data[i] = bgPixel[0];
          newImageData.data[i + 1] = bgPixel[1];
          newImageData.data[i + 2] = bgPixel[2];
          newImageData.data[i + 3] = bgPixel[3] ? (bgPixel[3] - 1) : 0;
        }
      }

      ctx.putImageData(newImageData, 0, 0);
      ctx = $canvas[0].getContext('2d');
      ctx.drawImage(maskCanvasScaled, 0, 0);
      maskCanvasScaled = ctx = imageData = newImageData = bctx = bgPixel = undefined;
    }

    var options={
      clearCanvas: false,
      color: function (word, weight) {
        return '#0F2D5D'
      },
      fontFamily: 'AvenirNextRegular',
      rotateRatio: 0,
      rotationSteps: 0,
      minSize:8,
      backgroundColor: '#fff',
      list:arr_new
      
    }
    //alert('before wc')
    WordCloud($canvas[0], options);
    setTimeout(function () {
    }, 100);
    //alert('after wc')
    var load = $("#loader").hide();
    var blank_ = $("#blank").hide();

} // end of run


 function makeCanvas(width_wc,height_wc,arr_new) {
    //alert('inside makecanvas')
    maskCanvas = null;
    var url='static/img/filled-circle.png'
    var img = new Image();
    img.src = url;

    img.onload = function readPixels() {
      //alert('inside image load')
      window.URL.revokeObjectURL(url);
      maskCanvas = document.createElement('canvas');
      maskCanvas.width = img.width;
      maskCanvas.height = img.height;

      var ctx = maskCanvas.getContext('2d');
      ctx.drawImage(img, 0, 0, img.width, img.height);

      var imageData = ctx.getImageData(
        0, 0, maskCanvas.width, maskCanvas.height);
      var newImageData = ctx.createImageData(imageData);

      for (var i = 0; i < imageData.data.length; i += 4) {
        var tone = imageData.data[i] +
          imageData.data[i + 1] +
          imageData.data[i + 2];
        var alpha = imageData.data[i + 3];

        if (alpha < 128 || tone > 128 * 3) {
          // Area not to draw
          newImageData.data[i] =
            newImageData.data[i + 1] =
            newImageData.data[i + 2] = 255;
          newImageData.data[i + 3] = 0;
        } else {
          // Area to draw
          newImageData.data[i] =
            newImageData.data[i + 1] =
            newImageData.data[i + 2] = 0;
          newImageData.data[i + 3] = 255;
        }
      }

      ctx.putImageData(newImageData, 0, 0);
    };
    //alert('end of image load')
    //run(width_wc,height_wc,arr_new)
    setTimeout(()=>{run(width_wc,height_wc,arr_new)}, 2000)

    

  } //end of makecanvas

/*ending of word cloud functions*/

$(document).ready(function(){
    $.ajax({
        'async': false,
        'global': false,
        'url': 'static/data/wordFrequencyFinal.csv',
        'dataType': "text",
        'success': function (data) {

            json_wc_data = d3.csv.parse(data);
            //console.log(json_wc_data)
            var arr=[]
            var arr_new=[]
            var min_ind;

            for (index in json_wc_data){
                arr.push([json_wc_data[index]['word'],parseInt(json_wc_data[index]['frequency'])])
            }        
            //arr.sort(compare);
            //console.log('initial array length--'+arr.length)

            //arr=arr.splice(0,400)
            //console.log(arr)
            var minWords1=d3.min(arr, function(d) {return d[1]})
            var maxWords1=d3.max(arr, function(d) {return d[1]})
            console.log("min-------"+minWords1)
            console.log("max-------"+maxWords1) 
            //console.log(arr)   
            var sizescale = d3.scale.linear().domain([minWords1,maxWords1]).range([10,110]);
            var sizescale2; 

            for (var b=0;b<arr.length;b++){
                if(sizescale(arr[b][1])<40){
                    min_ind=b
                    min_size=sizescale(arr[b][1])
                    sizescale2= d3.scale.log().domain([minWords1,arr[b][1]]).range([10,min_size]);
                    break
                }
            }
            //console.log(min_ind)
            for (var b=0;b<arr.length;b++){
                if(b<min_ind){
                    su=parseInt(sizescale(arr[b][1]))
                    arr_new.push([arr[b][0],su])
                }
                else {
                    su=parseInt(sizescale2(arr[b][1]))
                    arr_new.push([arr[b][0],su])
                }               
            }
            //console.log(arr_new)
            draw_word_cloud(arr_new)
    
        }
    });
});