var maxLevel=2



function setTable(data){
console.log(data.table);
var table=document.getElementById('recordTable');
checkboxes=table.getElementsByTagName('input')
for (i =0;i<checkboxes.length;i++){
	checkboxes[i].checked=data.table[i]
}
setPreview()
}




function checkboxClicked(data){
	node=$('#tree').treeview('getSelected')[0];
	node.table[parseInt(data.id)]=data.checked;
	row=Math.floor(parseInt(data.id)/6);
	
	var docSelector=document.getElementById('docSelector');
	docSelector.value=row;

	setPreview()
}


function setPreview(){
	var selectedNode=$('#tree').treeview('getSelected')[0];
	//console.log(selectedNode.nodeId)
	var textField=document.getElementById('previewField');
	var selectedDocument=document.getElementById('docSelector').value;
	highlightRow(selectedDocument);
	var rootNode=$('#tree').treeview('getNode', 0);
	


	

	
	//textField.innerHTML=getPreviewText(selectedNode,selectedDocument);
	textField.innerHTML=recursivePreview(rootNode,selectedDocument,maxLevel)
	//console.log(selectedNode.nodeId)

	var s=selectedNode.nodeId.toString()
	var relevantText=document.getElementsByName(s)[0]
	relevantText.scrollIntoView()
}




function getPreviewText(node,selectedDocument){
	//console.log(node.text)
	//console.log(node.table)
	var settings=node.table.slice(selectedDocument*6,selectedDocument*6+6);


	var res= (settings[0] ? node.text : "not displayed "+node.text)
	  + (settings[1] ? " "+node.credits : " ")
	  + (settings[2] ? " "+"[NOTE]" : " ")
	  + (settings[3] ? " "+"[SEMESTER]" : " ")
	  + (settings[4] ? " "+"[THEMA]" : " ")
	  + (settings[5] ? " "+"[TITEL]" : " ")

	return res
}



function recursivePreview(node,selectedDocument,level){
	//console.log(node.text+" at level "+level)
	var res="<p name="+node.nodeId+" style=\"margin-left: "+ ((maxLevel-level)*50) +"px\">"+getPreviewText(node,selectedDocument)+"</p>"
	if (node.nodes&&level>0){
		var i
		var count
		for ( i =0, count=node.nodes.length;i < count;i++){
			var n=node.nodes[i]
			//console.log(node.nodes)
			//console.log(i)
			//console.log("the name is"+n.text)
			res+=recursivePreview(n,selectedDocument,level-1)
		}
	}
	return res
}









function pageLoaded(){
	$('#tree').treeview('selectNode', 0);
	setPreview();
}



var changed=[]

function getChangedNodes(){
	changed=[]
	oRoot=c[0];
	root= $('#tree').treeview('getNode', 0);
	compare(root,oRoot);
	return changed
}


function compare(a,b){
	if(!equalTable(a,b)){
		changed.push({"name":a.text,"table":a.table})
	}
	if(a.nodes){
		var j;
		var len=a.nodes.length;
		for (j=0;j<len;j++){
			compare(a.nodes[j],b.nodes[j])
		}
	}
}




function equalTable(a,b){
	return (JSON.stringify(a.table)==JSON.stringify(b.table))
}


function saveButton(){
	xmlhttp = new XMLHttpRequest();
	xmlhttp.open("POST",'/save/0',true);
	xmlhttp.setRequestHeader("Content-type", "application/json");
	content=getChangedNodes()
		
	xmlhttp.send(JSON.stringify(content))

	console.log("save pressed")
}


function finishButton(){
	saveButton()
	window.location.href="/changes"
}



function highlightRow(doc){
	//console.log(doc)
	var table = document.getElementById("recordTable");
	var rows=table.getElementsByTagName("tr");
	for(x=0;x<rows.length;x++){

		if(x-1==doc){
			//console.log("row "+x+" highlighted")
			rows[x].style.backgroundColor="#99ccff";


		}
		else{
			//console.log("row "+x+" not highlighted")
			rows[x].style.backgroundColor="#ffffff";


		}
	}
}


var copyTable;

function copy(){
	node=$('#tree').treeview('getSelected')[0];
	copyTable=node.table;
}


function paste(){
	node=$('#tree').treeview('getSelected')[0];
	if(copyTable!=null){
		node.table=copyTable
		setTable(node)
	}

}

