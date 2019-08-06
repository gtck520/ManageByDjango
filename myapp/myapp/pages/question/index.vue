<template>
	<view>		
		<cu-custom bgImage="../../static/img/sylb2244.jpg" :isBack="true">
			<block slot="backText">返回</block>
			<block slot="content"></block>
		</cu-custom>
		<form>
														
					<view class="cu-bar bg-white solid-bottom" v-if="subjectData.is_end==false">
						<view class="action text-black">
							<text class="cuIcon-title text-red"></text>{{subjectData.content}}？
						</view>
					</view>
					<view>

						<radio-group class="block"  @change="RadioboxChange" v-if="subjectData.answer_type===0">
							<view class="cu-form-group" v-for="(option,index) in subjectData.subs" :key='index' v-if="option.content_type===2">
								<radio :value="option.id" :checked="setsubject[0]==option.id?true:false" ></radio>
								<view class="title text-black">{{index+1}}.{{option.content}}</view>
							</view>
						</radio-group>

						<checkbox-group class="block"  @change="CheckboxChange" v-else-if="subjectData.answer_type===1">
							<view class="cu-form-group" v-for="(option,index) in subjectData.subs" :key='index' >
								<checkbox :value="option.id" :checked="option.checked" v-if="option.content_type===2"></checkbox>
								<view class="title  text-black" v-if="option.content_type===2">{{index+1}}.{{option.content}}</view>
							</view>
						</checkbox-group>
								
						<view v-else-if="subjectData.answer_type===2">
							<view class="cu-form-group solid-bottom">
								<view class="title  text-black">
									答：
								</view>
								<input placeholder="文本输入框" name="input" @blur="textInput" :value="answer"></input>
							</view>
						</view>		
						<view class="padding" v-if="subjectData.is_end==false">				
							<button class="cu-btn block bg-blue margin-tb-sm lg" type="" @click="setAnwser" >确认</button>
						</view>
						<view class="padding" v-else>							
							<text class="text-black">{{subjectData.content}}</text>		
							<button class="cu-btn block bg-blue margin-tb-sm lg" type="" @click="setEnd" >确认</button>
						</view>
					</view>


		</form>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				answer:'',//作答答案
				answerid:0,//答题表id
				subjectId:0,//当前问题id
				subjectData:{},
				setsubject:[],//已作答答案内容
				nextid:0 //多选情况的 下一题id
			}
		},
		onReady() {

		},
		onLoad(o) {
			var Interid = o.id;
			this.getInteractives(Interid);
		},
		methods: {
			getInteractives(interid){//获取交互内容
				this.subjectId=interid;
				this.loading = true;
				this.nextid=0;
				this.$api.getInteractives(interid,{noncestr: Date.now()}).then((res)=>{
					this.loading = false;
					this.subjectData = res.data;
					// console.log(this.subjectData)
					let sublist = this.subjectData.subs;
					sublist.forEach(item=>{
						if(item.content_type===1){
							this.nextid=item.id;
						}
					})				
					
					this.getUserInteractives(interid);
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});		
			},		
			getUserInteractives(interid){//提取已作答内容
				this.loading = true;
				this.setsubject=[];
				this.answer='';
				this.answerid=0;
				this.$api.getAllInteractives('?hasdo=1&interid='+interid,{noncestr: Date.now()}).then((res)=>{
					this.loading = false;	
					this.answerid=res.data[0].id;
					this.answer=res.data[0].answer;					
					if(res.data[0].interactive.answer_type===0){//单选	
						this.setsubject.push(parseInt(res.data[0].answer));
					}
					else if(res.data[0].interactive.answer_type===1){//多选					
						this.setsubject = res.data[0].answer.split(",");
						let sublist = this.subjectData.subs;
						this.subjectData.subs=[];
						sublist.forEach(item=>{
							if(this.setsubject.indexOf(item.id.toString()) > -1){
								item.checked= true;
							}
							else{
								item.checked= false;
							}
							this.subjectData.subs.push(item);
						})				
					}else{
						this.setsubject.push(res.data[0].answer);
					}
				}).catch((err)=>{
					this.loading = false;
					this.answerid=0;
					console.log('request fail', err);
				});	
				
			},
			RadioboxChange : function(e) { //单选选中
				this.answer = e.detail.value;
			},
			CheckboxChange: function(e) { //复选选中
               var  values = e.detail.value;
			   this.answer = values.join(',');

			},
			textInput : function(e) { //填空题			
				this.answer = e.detail.value;				
			},
			setAnwser : function(){
				this.loading = true;
				var updateid = 0;
				if (this.setsubject.length == 0){				
					updateid = 0;
				}else {			
					updateid = this.answerid;
				}
				this.$api.setInteractives(updateid,{
					'has_read':true,
					'answer':this.answer,
					'interactive':this.subjectId,
				}).then((res)=>{
					this.loading = false;
					if(this.$api.islogin(res.data)){
						if(this.nextid>0){
							var nextid = this.nextid;
						}else
						{
							var nextid = this.answer;
						}						
						this.$api.getInteractives(nextid,{noncestr: Date.now()}).then((res)=>{
						// console.log(res.data.subs[0]['id']);
						if(this.nextid>0){//多选的情况，提取的为 子选项中内容类型为 问题的记录 作为下一条问题
							this.getInteractives(res.data.id);
						}else{
							this.getInteractives(res.data.subs[0]['id']);
						}
								
						});	
					}
					
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});	
				
			},
			setEnd:function(){
				uni.navigateTo({
					url: 'catalogue',
				})
			}
			
		}
	}
</script>

<style>
	@import "../../colorui/animation.css";
	page {
		background-color: #FFFFFF;
	}

	.cu-form-group {
		justify-content: flex-start
	}

	.cu-form-group .title {
		padding-left: 30upx;
		padding-right: 0upx;
	}

	.cu-form-group+.cu-form-group {
		border-top: none;
	}

	.cu-bar-title {
		min-height: 50upx;
	}
	
	.cu-list.menu>.cu-item-error{justify-content: flex-start;}
</style>
