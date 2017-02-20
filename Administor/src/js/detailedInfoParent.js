(function(){
  Vue.http.interceptors.push(function(request, next){
    request.credentials = true;
    next();
  });
	var vm = new Vue({
      el: 'body',
      data:{
      	timer: null,
        domain: 'http://www.yinzishao.cn:8000',
      	status:{
      		isSelecting: true,
	        isLoading: false,
	        isTutorInfo: false,
          isChangeInfo: false,
	        isRemindTeacher: false,
          isList: true,
          isNoList: false,
          text: '删除该请求',
          isSuccess: true,
          onParent: true,
          onTeacher: false,
          errorTip:'对不起，您只能选择一位老师'
      	},
      	detailedList:{
      		pd_id:0,
      		name:'张先生',
      		teacher_sex: '不限',
          learning_phase: '高中',
      		aim:'提高成绩',
      		subject:'数学',
          subject_other: '',
      		grade:'高一',
      		address:"大学城小洲",
      		time:"周六上午",
      		class_field: '成绩优良',
      		teacher_method:"nice,细心",
          teacher_method_other: '',
      		require:"上课要耐心细致，对孩子好",
      		salary: '18/h',
      		bonus: '100/月',
      		deadline: '2016年12月23号',
      		tel: '1234567891'
      	},
      	msgList:[],
        jsonData: [],
      	msgDetailedList: [],
        start: 0,
      	msg: {
      		text: '已发送请求'
      	},
        form:{
          selected:'',
          isRegister: '',
          isMsg: '',
        } 
      },
      ready: function(){
          this.renderTutor();
          this.renderOrderData();
          this.status.isLoading = true;
      },
      methods: {
        down: function(){
          this.start++;
          if(this.jsonData.length!==0){
            this.renderOrderData();
          }
        },
      	renderOrderData: function(){
          this.status.isSelecting = true;
          var id = parseInt(this.getParam('listId'));
          this.$http.post(this.domain+'/getUserOrders',{
            "id":id,
            "user":"parent",
            "start":this.start,
            "size":6
          },{
            crossOrigin: true,
            headers:{
              'Content-Type':'application/json' 
            }
          }).then(function(res){
          	console.log(res.json());
            if(res.json().success == 0){
              console.log(res.json().error);
            }else{
              this.jsonData = res.json();
              var data = res.json();
              if(data.length!=0){
                for(var i = 0;i<data.length;i++){
                  if(data[i].result == '您已拒绝'||data[i].result == '老师已拒绝'){
                    data[i].isRed = true;
                  }else{
                    data[i].isRed = false;
                  }
                 }
                var json=this.msgList.concat(data);
                this.$set('msgList',json);
                this.status.isSelecting = false;
              }else{
                if(this.msgList.length==0){
                  this.status.isNoList = true;
                  this.status.isList = false;
                }
              }
            }
          });
		    },
        grade_level: function(key){
          switch(key){
            case 0:
              return '';
            case 1:
              return '较为靠后';
            case 2: 
              return '中等偏下';
            case 3:
              return '中等水平';
            case 4:
              return '中上水平';
            case 5: 
              return '名列前茅';
          }
        },
		    getParam: function(param) {   //获取url上的参数
          var str = location.search;
          if (str.indexOf("?") == -1) return '';
          str = str.substr(1, str.length).split("&");
          for (var i = 0, cell, length = str.length; i < length; i++) {
            cell = str[i].split('=');
            if (cell[0] == param) {
              return cell[1];
            }else{
              // return false;
            }
          }
        },
  	    renderTutor: function(){
  	      var id = parseInt(this.getParam('listId'));
  	      this.$http.post(this.domain+'/getInfo',{
              'id': id,
              'format': true,
              'user': 'parent'
          },{
          crossOrigin: true,
        	headers:{
            'Content-Type':'application/json' 
          }
        }).then(function(res){
        	console.log(res.json());
          if(res.json().sucess == 0){
            console.log(res.json().error);
          }else{
            var data = res.json();
            data.class_field=this.grade_level(data.class_field);
            this.$set('detailedList',data);
          }
        });
  	    },
        onReturn: function(){
          var searchWord,word = this.getParam('keyword');
          if(word){
            searchWord = word;
          }else{
            searchWord = '';
          }
          console.log(this.getParam('keyword'),searchWord);
          if(!this.getParam('list')){
            window.location.href = './userAdministor.html?user=parent&keyword='+searchWord;
            
          }else{
            window.location.href = './myList.html';
          }
        },
        onUser:function(){
      		window.location.href = './userAdministor.html';
      	},
      	onDeal: function(){
          window.location.href = './deal.html';
      	},
      	onOther: function(){
          window.location.href = './other.html';
      	},
      	onChangeRequest: function(index){
      		window.location.href='./parentQuestion.html?changeInfoId='+index;
      	},
      	onRemindParent: function(index){
      		this.status.isRemindTeacher = true;
          var self = this;
      		this.timer && clearTimeout(this.timer);
    			this.timer = setTimeout(function(){
    				self.status.isRemindTeacher = false;
    			}, 1000);
      		if(this.msg.text=='已发送请求'){
      			this.$http.post(this.domain+'/remindFeedBack',{
	              'id': index,
	              'user':'parent',
	            },{
                crossOrigin: true,
	              headers:{
	                'Content-Type':'application/json; charset=UTF-8' 
	              }
	            }).then(function(res){
                console.log(res.json());
	              if(res.json().success == 1){
	              	this.msg.text = '请勿重复发送请求';
	              }
	            })
      		}
      	},
      	onDetailedInfo: function(index){
           this.form.selected = index;
           this.status.text = '删除该请求';
           this.msgDetailedList = [];
           var list = this.msgList[index];
           this.$http.post(this.domain+'/getTeacherInfo',{
              "tea_id": list.tea,
              "format": true,
            },{
              crossOrigin: true,
              headers:{
                'Content-Type':'application/json'  
              }
            }).then(function(res){
               if(res.json().success == 0){
                console.log(res.json().error);
               }else{
                var data = res.json();
                if(data.certificate_photo!=''||data.certificate_photo!=null){
                  data.certificate_photo=this.domain+data.certificate_photo;
                }
                var photo=data.teach_show_photo,len = photo.length;
                if(len>0){
                 for(var i=0;i<len;i++){
                  photo[i]=this.domain+photo[i];
                 }
                }
                if(list.expectation!=null||list.expectation!=''){
                  data.expectation=list.expectation;
                }
                this.msgDetailedList = data;
                this.status.isTutorInfo = true;
               }
            })
            this.status.onParent = true;
            this.status.onTeacher = false;
            this.status.isSuccess = true;
            if(list.result == '管理员审核中'){
              this.form.isRegister = "管理员审核中";
            }else if(list.result == '已成交'){
              this.form.isRegister = "双方已成交";
            }else if(list.result == '您已邀请'){
              this.status.isSuccess = false;
              this.form.isRegister = "取消邀请";
            }else if(list.result == '您已拒绝'){
              this.status.isSuccess = false;
              this.form.isRegister = "您已拒绝该老师";
            }else if(list.result == '老师已拒绝'){
              this.status.isSuccess = true;
              this.form.isRegister = "再次邀请该老师";
            }
            else if(list.result == '向您报名'){
              this.status.onParent= false;
              this.status.onTeacher = true;
            }else if(list.result == '您已同意'){
              this.status.isSuccess = false;
              this.form.isRegister = "拒绝选择该老师";
            }
      	},
      	onDelete: function(index){        	
      		this.$http.post(this.domain+'/deleteOrder',{
              'oa_id': this.msgList[index].oa_id,
            }, {
            crossOrigin: true,
    				headers:{
              'Content-Type':'application/json' 
            } 
    			}).then(function(res) {
    				if (res.json().success == 1) {
              var self = this;
              this.status.text = '该请求已删除';
              this.timer && clearTimeout(this.timer);
              this.timer = setTimeout(function(){
                self.msgList.splice(index,1);
                self.status.isTutorInfo = false;
              }, 800);
    				}else{
              console.log(res.json().error);
            }
    				
    			});        
        },
        onRegister1: function(index){
         if(this.form.isRegister == "取消邀请"){
            this.form.isMsg = '邀请';
            this.status.isTutorInfo = false;
            this.status.isChangeInfo = true;
          }else if(this.form.isRegister == '再次邀请该老师'){
            this.$http.post(this.domain+'/inviteTeacher',{
              'tea_id': this.msgList[index].tea,
              'type': 1
            },{
              crossOrigin: true,
              headers:{
                'Content-Type':'application/json' 
              }

            }).then(function(res){
              console.log(res.json());
              if(res.json().success==1){
                this.form.isRegister = '您已邀请';
                this.msgList[index].finish = 0;               
                var self = this;
                this.timer && clearTimeout(this.timer);
                this.timer = setTimeout(function(){
                  self.msgList[index].result = '您已邀请';
                  self.msgList[index].isRed = false;
                  self.status.isTutorInfo = false;
               }, 1500);
              }else{
                console.log(res.json().error);
                var self = this;
                this.status.errorTip = res.json().error;
                this.status.isTutorInfo = false;
                this.status.isInfoTipOne = true;
                this.timer && clearTimeout(this.timer);
                this.timer=setTimeout(function(){
                self.status.isInfoTipOne = false;
                },2000);
              }
              
            })
          }else if(this.form.isRegister == '拒绝选择该老师'){
            this.status.isTutorInfo = false;
            this.form.isMsg = '信息';
            this.status.isChangeInfo = true;
          }else{
            this.status.isTutorInfo = false;
            return false;
          }
        },
        //选择该老师
        onSelect: function(index){
            this.$http.post(this.domain+'/handleOrder',{
            'type': 1,
            'id': this.msgList[index].tea,
            'accept': 1
          },{
            crossOrigin: true,
            headers:{
              'Content-Type':'application/json' 
            }

          }).then(function(res){
            if(res.json().success==1){
              var self = this;
              this.timer && clearTimeout(this.timer);
              this.timer = setTimeout(function(){
                self.status.isTutorInfo = false;
                self.msgList[index].result = "您已同意"; 
                self.msgList[index].isRed = false;             
              }, 1000);
            }else{
              console.log(res.json().error);
            }
          })
        },
        //拒绝该老师
        onRefuse: function(index){
          this.$http.post(this.domain+'/handleOrder',{
            'type': 1,
            'id': this.msgList[index].tea,
            'accept': 0
          },{
            crossOrigin: true,
            headers:{
              'Content-Type':'application/json' 
            }

          }).then(function(res){
            console.log(res.json());
              if(res.json().success==1){
              var self = this;
              this.msgList[index].finish = 1;
              this.timer && clearTimeout(this.timer);
              this.timer = setTimeout(function(){
                self.status.isTutorInfo = false;
                self.msgList[index].result = "您已拒绝";  
                self.msgList[index].isRed = true;            
              }, 1000);
            }else{
              console.log(res.json().error);
            }
          })
        },
        onSureChange: function(index){
          var msg = this.form.isMsg;
          if(msg == '邀请'){
            this.$http.post(this.domain+'/inviteTeacher',{
              'tea_id': this.msgList[index].tea,
              'type': 0
            },{
              crossOrigin: true,
              headers:{
                'Content-Type':'application/json' 
              }

            }).then(function(res){
              console.log(res.json());
              if(res.json().success==1){
                var self = this;
                  this.timer && clearTimeout(this.timer);
                  this.timer = setTimeout(function(){
                    self.status.isChangeInfo = false;
                    self.msgList.splice(index,1);              
                  }, 300);
              }else{
                console.log(res.json().error);
              }
              
            })
          }else{
            this.$http.post(this.domain+'/handleOrder',{
              'type': 1,
                'id': this.msgList[index].tea,
                'accept': 0
            },{
              crossOrigin: true,
              headers:{
                'Content-Type':'application/json' 
              }

            }).then(function(res){
              console.log(res.json());
              if(res.json().success==1){
                this.status.isChangeInfo = false;
                  this.msgList[index].result = '您已拒绝';
                  this.msgList[index].isRed = true; 
                  this.msgList[index].finish = 1;
              }else{
                console.log(res.json().error);
              }
            })
          }
          
        },
        onClose: function(){
        	this.status.isChangeInfo = false;
          this.status.isTutorInfo = false;
          this.status.isInfoTipOne = false;
        }
      },
	});
})();