function displayWindowSize(){
    
    var collection = [];
    var w = document.documentElement.clientWidth;
    var h = document.documentElement.clientHeight;
    
    collection.push(w);
    collection.push(h);

    return collection;
}