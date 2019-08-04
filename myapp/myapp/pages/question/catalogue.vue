<template>
	<view>
		<cu-custom bgImage="https://image.weilanwl.com/color2.0/plugin/sylb2244.jpg" :isBack="true">
			<block slot="backText">返回</block>
			<block slot="content">目录</block>
		</cu-custom>	
		<view  class="padding ">
			<view v-for="(item,index) in catalogues" :key="index"  class="padding-lr bg-white" :class="index>0?'margin-top':''" @click="gotoInteractives" :data-classid="item.id">
				<view class="solid-bottom padding">
					<text class="text-black">{{item.name}}</text>
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				catalogues:[]
			}
		},
		onLoad(options){
			this.getCatalogue();
		},
		methods: {
			getCatalogue(){
				// 获取目录列表
				this.loading = true
				this.$api.getCatalogue({noncestr: Date.now()}).then((res)=>{
					this.loading = false;
					this.catalogues=res.data;
					console.log(this.catalogues)
					
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});
				
			},
			gotoInteractives(e){
				// 获取目录列表
				let classid = e.currentTarget.dataset.classid; 
				this.loading = true;
				
				//提取已回答的问题记录
				this.$api.getAllInteractives('?hasdo=1',{noncestr: Date.now()}).then((res)=>{
					this.loading = false;
					//跳转到最后回答的问题
					uni.navigateTo({
						url: 'index?id='+res.data[0].interactive.id
					})
					
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
					this.$api.gotoInteractives(classid,{noncestr: Date.now()}).then((res)=>{
						this.loading = false;
						if(res.data.content=="")
						{
							uni.showModal({
								title: '提示',
								content: '该章暂无题目',
								showCancel:false,
								success: function (res) {
									
								}
							});
							return false;
						}else{
							uni.navigateTo({
								url: 'index?id='+res.data.id
							})
						}
						
					}).catch((err)=>{
						this.loading = false;
						console.log('request fail', err);
					});
				});
				
				
			}
			
		}
	}
</script>

<style>

</style>
