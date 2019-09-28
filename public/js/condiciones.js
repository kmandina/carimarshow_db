
	function condiciones(){
			var el = document.getElementById('terminosLink');
			if(el.fireEvent){
				el.fireEvent('onclick')
			}else{
			var evObj = document.createEvent('Events');
			evObj.initEvent('click',true,false);
			el.dispatchEvent(evObj);
			}
			}