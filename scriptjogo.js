var canvas, contexto, altura, largura, frames=0, subir = 0, descer = 0, velocidade = 4,estadojogo=0,pontuacao=0,level=200;
statusjogo = {
    play: 0, jogando:1, fim:2};
quadrado = {
    x:30,y:0,
    cor:"#800000",
    altu:(window.innerHeight/12),
    largu:(window.innerHeight/12),
    desenha: function(){
        contexto.fillStyle = this.cor;
        contexto.fillRect(this.x,this.y,this.altu,this.largu);
        if(quadrado.y <= canvas.height-quadrado.altu){quadrado.y += descer};
        if(quadrado.y > 0){quadrado.y = quadrado.y + subir};
    }
};

obstaculos = {
    obsta:[],
    cores:["#000080","#191970","#008B8B","#4B0082","#7B68EE","#00CED1"],
    tempoObs:0,    
    insere: function(){
        var Altu = 40+Math.floor((altura/2) * Math.random());
        var Altu2 = (altura-Altu);
        var vetory = [Altu2,0];
        this.obsta.push({
            x:largura,
            largura:30,
            altura: Altu,
            cor: this.cores[Math.floor(6 * Math.random())],
            y:vetory[Math.floor(2 * Math.random())]
            });
            this.tempoObs = 70;
    },
    atualiza:function(){
        this.tempoObs === 0 ? this.insere() : this.tempoObs--;
        for(var i=0,tam=this.obsta.length;i<tam;i++){
            var obs = this.obsta[i];
            if (pontuacao > level){ velocidade++; level+=200;}
            obs.x-=velocidade;
            if((quadrado.y <= (obs.y+obs.altura) && quadrado.y >= obs.y || quadrado.y <= obs.y && (quadrado.y+quadrado.altu)>= obs.y  )&& obs.x <= (quadrado.x+quadrado.largu) &&  obs.x >= quadrado.x){
               estadojogo=2;            
            }
            else if(obs.x < -50){ this.obsta.splice(i, 1); i--; tam--; }pontuacao+=0.1;}
        
    },
    desenha: function(){
        for(var i=0,tam=this.obsta.length; i<tam;i++){
            var obs = this.obsta[i];
            contexto.fillStyle = obs.cor;
            contexto.fillRect(obs.x,obs.y,obs.largura, obs.altura);
        }
    }
}

function clique(){
    if(estadojogo==statusjogo.play){estadojogo=statusjogo.jogando}
    else if(estadojogo===statusjogo.fim){estadojogo=0;obstaculos.obsta=[];quadrado.x=10;quadrado.y=0;}
    else{ if(descer===0 && subir===0){subir = -5;}
    aux=subir*-1; subir=descer*-1; descer=aux;}}

function botao(){
    var tecla = event.keyCode;
  
}

function main(){
    altura = window.innerHeight/1.5;
    largura = window.innerWidth/1.5;
    canvas = document.createElement("canvas");
    canvas.width=largura;
    canvas.height=altura;
    canvas.style.border="2px solid #000";
    contexto= canvas.getContext("2d");
    document.body.appendChild(canvas);
    document.addEventListener("mousedown",clique);
    document.addEventListener("keydown",botao);
    roda();}    

function desenha(){
    contexto.fillStyle ='#B0E0E6';
    contexto.fillRect(0, 0, largura, altura);
    quadrado.desenha();
    if(estadojogo===statusjogo.jogando){ 
        obstaculos.desenha();
        obstaculos.atualiza();
        contexto.font = `${altura/20}px Arial`;
        contexto.fillStyle = "black";
        contexto.fillText(`PONTOS:${Math.floor(pontuacao)} LVL${level/200}`,largura/2,altura/15,200,200);
       }else if(estadojogo===statusjogo.fim){
            contexto.fillStyle = "red";
            contexto.fillRect((largura/2)-(largura/3),(altura/2)-(altura/4),(largura/1.5),(altura/2));
            contexto.fillStyle = "black";
            contexto.lineWidth = 2;
            contexto.strokeRect((largura/2)-(largura/3),(altura/2)-(altura/4),(largura/1.5),(altura/2));
            contexto.fillStyle = "white";
            contexto.font = `${altura/20}px Arial`;
            contexto.fillText(`FIM DE JOGO   PONTOS:${Math.floor(pontuacao)}`,(largura/2)-(largura/7),(altura/2)-(altura/10));
            contexto.fillText(`CLIQUE PARA REINICIAR`,(largura/2)-(largura/7),(altura/2)+(altura/10));
    }else{
        pontuacao=0; level=200; velocidade=4;
        contexto.fillStyle = "green";
        contexto.fillRect((largura/2)-(largura/4),(altura/2)-(altura/10),(largura/2),(altura/5));
        contexto.fillStyle = "black";
        contexto.lineWidth = 2;
        contexto.strokeRect((largura/2)-(largura/4),(altura/2)-(altura/10),(largura/2),(altura/5));
        contexto.fillStyle = "white";
        contexto.font = `${altura/10}px Arial`;
        contexto.fillText("PLAY",(largura/2.3),altura/1.9);
    };}
function roda(){desenha(); window.requestAnimationFrame(roda);}
main();