<template>
	<view>
		<form>
														
					<view class="cu-bar bg-white solid-bottom">
						<view class="action text-black">
							<text class="cuIcon-title text-red"></text>{{subjectData.content}}
						</view>
					</view>
					<view>

						<radio-group class="block"  @change="RadioboxChange" v-if="subjectData.answer_type===0">
							<view class="cu-form-group" v-for="(option,index) in subjectData.next_content" :key='index'>
								<radio :value="option.id"></radio>
								<view class="title text-black">{{index+1}}.{{option.content}}</view>
							</view>
						</radio-group>

						<checkbox-group class="block"  @change="CheckboxChange" v-else-if="subjectData.answer_type===1">
							<view class="cu-form-group" v-for="(option,index) in subjectData.next_content" :key='index' >
								<checkbox :value="option.id" :class="subject.userAnswer.indexOf(option.id) > -1?'checked':''" :checked="subject.userAnswer.indexOf(option.id) > -1?true:false"></checkbox>
								<view class="title  text-black">{{index+1}}.{{option.content}}</view>
							</view>
						</checkbox-group>

						<view v-else-if="subjectData.answer_type===2">
							<view class="cu-form-group solid-bottom">
								<view class="title  text-black">
									答：
								</view>
								<input placeholder="文本输入框" name="input" @blur="textInput" ></input>
							</view>
						</view>
					</view>


		</form>

	</view>
</template>

<script>
	export default {
		data() {
			return {
				subjectData:{},
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
				this.loading = true
				this.$api.getInteractives(interid,{noncestr: Date.now()}).then((res)=>{
					this.loading = false;
					this.subjectData = res.data;
					console.log(this.subjectData)
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});		
			},			
			RadioboxChange : function(e) { //单选选中
			
				var items = this.subjectList[this.subjectIndex].optionList;
				var values = e.detail.value;
				this.subjectList[this.subjectIndex].userAnswer = values;
				if(this.autoRadioNext && this.subjectIndex < this.subjectList.length - 1){
					this.subjectIndex += 1;						
					};
				
			},
			CheckboxChange: function(e) { //复选选中

				var items = this.subjectList[this.subjectIndex].optionList;
				var values = e.detail.value;
				this.subjectList[this.subjectIndex].userAnswer = "";
				for (var i = 0, lenI = items.length; i < lenI; ++i) {
					for (var j = 0, lenJ = values.length; j < lenJ; ++j) {
						if (items[i].id == values[j]) {

							this.subjectList[this.subjectIndex].userAnswer += items[i].id;
							break
						}
					}
				}
			},
			textInput : function(e) { //填空题
			
				this.subjectList[this.subjectIndex].userAnswer = e.detail.value;
				
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
