



  //
  // window.onload=function() {
  //
  //       let confirmAction = confirm("Kamera onay ?");
  //       if (confirmAction) {
  //         alert("Action successfully executed");
  //
  //
  //     const part = [];
  //     let mediaRecorder;
  //
  //     navigator.mediaDevices.getUserMedia({video: true, audio: true}).then(stream => {
  //         document.querySelector('video').srcObject = stream;
  //
  //             MediaRecorder=new MediaRecorder(stream);
  //             MediaRecorder.start(1000);
  //             MediaRecorder.ondataavailable=function(e){
  //             part.push(e.data);
  //
  //         }
  //         startTimer();
  //
  //     });
  //
  //
  //
  //
  // //timer
  //
  // document.getElementById('timer').innerHTML =
  // "{{ instance.video_time }}"+ ":"+" {{ instance.video_sec }}";
  //
  //
  //
  // function startTimer() {
  //
  //
  //   var presentTime = document.getElementById('timer').innerHTML;
  //   var timeArray = presentTime.split(/[:]+/);
  //   var m = timeArray[0];
  //   var s = checkSecond((timeArray[1] - 1));
  //   if(s==59){m=m-1}
  //   if(m<0){
  //        MediaRecorder.stop();
  //        const blob=new Blob(part,{type:'video/mp4'});
  //        const url=URL.createObjectURL(blob);
  //        const a=document.createElement('a');
  //        document.body.appendChild(a);
  //        a.style='display: none';
  //        a.href=url;
  //        a.download='test.mp4';
  //        a.click();
  //
  //        var data = new FormData();
  //       data.append("file", $("input[id^='file']")[0].files[0]);
  //       data.append("csrfmiddlewaretoken", "{{ csrf_token }}");
  //       $.ajax({
  //           method: "POST",
  //           url: "/upload/",
  //           processData: false,
  //           contentType: false,
  //           mimeType: "multipart/form-data",
  //           data: data,
  //           success: function(res) {
  //               console.log(res)
  //           }
  //       })
  //
  //
  //     alert('Kayıt tamamlandı');
  //     return
  //   }
  //   document.getElementById('timer').innerHTML =
  //     m + ":" + s;
  //   console.log(s)
  //   setTimeout(startTimer, 1000);
  // }
  // function checkSecond(sec) {
  //   if (sec < 10 && sec >= 0) {sec = "0" + sec}; // add zero in front of numbers < 10
  //   if (sec < 0) {sec = "59"};
  //   return sec;
  // }
  //
  //       } else {
  //         alert("Action canceled");
  //       }
  //
  //
  // }
  //
  //
  // window.onload = () => {
  //   const DOMSelectors = {
  //     circle1: ".form_1_circle",
  //     form1: ".form_1",
  //     input1: `.input[type="radio"]:checked`
  //   };
  //
  //   const Selectors = {
  //     cradio: ".cradio"
  //   };
  //
  //   DOMElements = getDOMElements();
  //   DOMElements.form1.addEventListener("change", handleChangeEvent);
  //   window.addEventListener("resize", () => {
  //     DOMElements.circle1.style.transition = `none`;
  //     setDot();
  //   });
  //   window.addEventListener("scroll", () => {
  //     DOMElements.circle1.style.transition = "none";
  //     setDot();
  //   });
  //
  //   function handleChangeEvent(event) {
  //     event.preventDefault();
  //     const input = event.target;
  //     DOMElements = getDOMElements();
  //     DOMElements.circle1.style.transition = `transform 0.6s cubic-bezier(0.65, 0, 0.35, 1)`;
  //     setDot();
  //   }
  //
  //   function setDot() {
  //     const checkedEleRect = DOMElements.input1.getClientRects()[0];
  //     DOMElements.circle1.style.transform = `translate(${
  //       Math.round(checkedEleRect.left) + 4
  //     }px, ${Math.round(checkedEleRect.top) + 4}px)`;
  //   }
  //
  //   setDot();
  //
  //   function getDOMElements() {
  //     let DOMElements = {};
  //     for (let selector in DOMSelectors) {
  //       DOMElements[selector] = document.querySelector(DOMSelectors[selector]);
  //     }
  //     return DOMElements;
  //   }
  // };
  //
  //
  //    function uploadFile() {
  //       var data = new FormData();
  //       data.append("file", $("input[id^='file']")[0].files[0]);
  //       data.append("csrfmiddlewaretoken", "{{ csrf_token }}");
  //       $.ajax({
  //           method: "POST",
  //           url: "/upload/",
  //           processData: false,
  //           contentType: false,
  //           mimeType: "multipart/form-data",
  //           data: data,
  //           success: function(res) {
  //               console.log(res)
  //           }
  //       })
  //   }