    if(M.isIE) alert("ie不支持canvas,请用chrome和Safari浏览,Firefox也可以,但是性能可能有问题")
    /**
     * 精灵对象,类似flash(ActionScript3.0)中的精灵.
     * 所有的动画元素都必须继承自此对象,继承之后自动拥有move方法和速度属性
     * 每个动画元素都必须拥有一个自己的特殊的draw()方法的实现,这个方法用来在渲染每一帧的时候指定自己如何呈现在canvas帧画布上
     * 注意这个所谓的"帧画布"不是指原生的canvas元素,而是指下面定义的一个Canvas对象,此对象的意义就是一个帧,它负责把需要在这一帧上呈现的
     * 图形画在canvas上,然后每一帧开始的时候都会清除上次画的,类似flash中的帧概念
     *
     * 
     */
    var Sprite=function(){
        this.speed={
            x:1,
            y:1
        }
    }
    Sprite.prototype={
        /**
         *每个精灵都必须有自己的draw实现
         */
        draw:function(){

        },
        /**
         *无需单独实现,通用的动画函数
         */
        move:function(){
            this.x+=this.speed.x;
            this.y+=this.speed.y;
            if(this.childs!=null&&this.childs.length>0){
                for(var i=0;i<this.childs.length;i++){
                    this.childs[i].speed=this.speed;
                    this.childs[i].move();
                }
            }
        },
        /**
         *向此精灵添加一个子精灵
         */
        appendChild:function(sprite){
            if(this.childs==null) this.childs=[]
            this.childs.push(sprite)
        },
        /**
         *渲染子精灵
         */
        drawChild:function(){
            if(this.childs!=null&&this.childs.length>0){
                for(var i=0;i<this.childs.length;i++){
                    this.childs[i].draw();
                }
            }
        }
    }
    /**
     * 圆对象
     *
     * @param {Content2d} 一个canvas实例
     * @param {number} 初始x坐标
     * @param {number} 初始y坐标
     * @param {number} 半径
     * @param {json} 配置信息
     */
    var Circle=function(ctx,x,y,radius,config){
        this.ctx=ctx;
        this.x=x;
        this.y=y;
        this.radius=radius;
        this.config={
            strokeStyle:"#000",
            lineWidth:"1"
        }
        M.dom.mixin(this.config, config)
    }
    Circle.prototype=new Sprite();
    /**
     *draw方法的实现
     */
    Circle.prototype.draw=function(){
        this.ctx.beginPath();
        this.ctx.lineWidth = this.config.lineWidth;
        this.ctx.strokeStyle =this.config.strokeStyle;
        this.ctx.arc(this.x,this.y,this.radius,0,Math.PI*2,true)
        this.ctx.stroke();
        this.drawChild();
    }
    /**
     * 矩形对象
     *
     * @param {Content2d} 一个canvas实例
     * @param {number} 初始x坐标
     * @param {number} 初始y坐标
     * @param {number} 宽
     * @param {number} 高
     * @param {json} 配置信息
     */
    var Rect=function(ctx,x,y,width,height,config){
        this.ctx=ctx;
        this.x=x;
        this.y=y;
        this.width=width;
        this.height=height;
        this.config={
            fillStyle:"#000",
            lineWidth:"1"

        }
        M.dom.mixin(this.config, config)
    }
    Rect.prototype=new Sprite()
    Rect.prototype.draw=function(){
        this.ctx.beginPath();
        this.ctx.lineWidth = this.config.lineWidth;
        this.ctx.fillStyle =this.config.fillStyle;
        this.ctx.fillRect (this.x, this.y, this.width, this.height,false);
        this.ctx.stroke();
        this.drawChild();
    }
    /**
     * 正方形对象
     *
     * @param {Content2d} 一个canvas实例
     * @param {number} 初始x坐标
     * @param {number} 初始y坐标
     * @param {number} 边长
     * @param {json} 配置信息
     */
    var Square=function(ctx,x,y,size,config){
        this.ctx=ctx;
        this.x=x;
        this.y=y;
        this.width=size;
        this.height=size;
        this.config={
            fillStyle:"#000",
            lineWidth:"1"
        }
        M.dom.mixin(this.config, config)
    }
    Square.prototype=new Rect();

    /**
     * 图形容器对象
     *
     * @param {Content2d} 一个canvas实例
     * @param {number} 初始x坐标
     * @param {number} 初始y坐标
     * @param {number} 宽
     * @param {number} 高
     * @param {json} 配置信息
     */
    var Img=function(ctx,img,x,y,width,height,config){
        this.ctx=ctx;
        this.img=img
        this.x=x;
        this.y=y;
        this.width=width;
        this.height=height;
        this.config={
        }
        M.dom.mixin(this.config, config)
    }
    Img.prototype=new Rect();
    Img.prototype.draw=function(){
        this.ctx.drawImage(this.img,this.x,this.y,this.width,this.height);
        this.drawChild();
        //    this.ctx.stroke();
    }
    /**
     *帧对象,每隔一段时间重画自己一次,类似flash中的帧概念
     *原理就是每到一定时间就清除canvas,然后调用当前帧里的所有的动画元素的draw()方法,将所有动画元素按照新的配置重画
     *从而生成动画,之后程序无需关心元素的重画,只需要调整元素属性即可,这个对象会自动管理元素的渲染
     *
     */
    var Canvas=function(){
        this.interval=null;
        this.sprites=[]
    }
    /**
     *
     */
    Canvas.prototype={
        /**
         * 开始动画
         */
        begin:function(){
            this.interval=setInterval((function(param){
                return function(){param.render();}
            })(this),20);
        },
        /**
         *渲染
         */
        render:function(){
            //    M.trace(this.sprites.length)
            this.ctx.clearRect(-800, -800, 1600, 1600)
            for(var i in this.sprites){
                if(typeof(this.sprites[i])=="function") continue;
                this.sprites[i].draw();
            }
        },
        /**
         *添加动画元素
         */
        addSprite:function(name,sprite){
            this.sprites[name]=sprite;
        },
        /**
         * 停止动画
         */
        stop:function(){
            clearInterval(this.interval)
        },
        clear:function(){
            for(var i in this.sprites){
                if(typeof(this.sprites[i])=="function") continue;
                if(this.sprites[i].x>800&&this.sprites[i].y>800){
                    delete this.sprites[i]
                }
            }
        }
    }
    var ctx=$("canvas").getContext('2d');
    var can=new Canvas();
    can.ctx=ctx;
    can.begin();
    var m=M.Math;
    /**
    setInterval(function(){
        for(var i in can.sprites){
            if(typeof(can.sprites[i])=="function") continue;
            can.sprites[i].move()
        }
    },20)
    
    var circle=new Circle(ctx,100,100,100,{
        strokeStyle:M.dom.getRandomColor(),
        lineWidth:Math.random()*5
    })

    can.addSprite(1, circle)
    var circle2=new Circle(ctx,100,100,50,{
        strokeStyle:M.dom.getRandomColor(),
        lineWidth:Math.random()*5
    })

    circle.appendChild(circle2)
    var circle3=new Circle(ctx,50,60,20,{
        strokeStyle:M.dom.getRandomColor(),
        lineWidth:Math.random()*5
    })
    circle2.appendChild(circle3)
*/
    var count=0
    var img=new Image()
    img.src="http://mier.googlecode.com/files/0fixed.gif"
    img.onload=function(){
        setInterval(function(){
            can.clear()
            var circle=new Circle(ctx,0,0,m.random(30),{
                strokeStyle:M.dom.getRandomColor(),
                lineWidth:Math.random()*5
            })
            circle.speed={x:m.randomD(4),y:m.randomD(4)}
            can.addSprite(count++, circle)
            var rect=new Square(ctx,0,0,m.random(40),{
                fillStyle:M.dom.getRandomColor(),
                lineWidth:Math.random()*5
            })

            rect.speed={x:m.randomD(4),y:m.randomD(4)}
            can.addSprite(count++, rect)
            var img1=new Img(ctx,img,0,0,24,24,{
                fillStyle:M.dom.getRandomColor(),
                lineWidth:Math.random()*5
            })

            img1.speed={x:m.randomD(4),y:m.randomD(4)}
            can.addSprite(count++, img1)
        },400)
        ctx.translate(400,400)
        setInterval(function(){
            for(var i in can.sprites){
                  if(typeof(can.sprites[i])=="function") continue;
                can.sprites[i].move()
            }
        },20)
        M.dom.on(document, "mousemove", function(e){
            var e=e||window.event;
            var pos=M.dom.getMousePos(e);
            ctx.rotate((Math.PI*2/360)*((pos.y-400)/100))
        })
    }
