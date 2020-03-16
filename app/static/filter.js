function filter(){
	input=document.getElementById('search').value.toUpperCase();
	console.log(input);

	list=document.getElementById('cardlist');
	card=list.getElementsByClassName('card');
	cardtitle=list.getElementsByClassName('card-title');
	for (var i = 0; i < card.length; i++) {
		title=cardtitle[i].innerText;
		if(title.toUpperCase().indexOf(input)>-1){
			card[i].style.display="";
		}
		else{
			card[i].style.display="none";
		}
	}
}



