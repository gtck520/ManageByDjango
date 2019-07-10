<template>
	<view class="content">
		
	</view>
</template>

<script>
	export default {
		data() {
			return {
			}
		},
		onLoad(){
			this.loadExecution()
		},
		methods: {
			loadExecution: function(){
				/**
				 * 获取本地存储中launchFlag的值
				 * 若存在，说明不是首次启动，直接进入首页；
				 * 若不存在，说明是首次启动，进入引导页；
				 */
				var launchFlag='';
				uni.getStorage({
					key: 'launchFlag',
					success: function (sto) {
						launchFlag=sto.data
					}
				});
				// 判断launchFlag的值是否为true，如果是true进入首页
				if(launchFlag == true){
					uni.switchTab({
						url: '/pages/tabbar/tabbar-1/tabbar-1'
					});
				}else{
					// launchFlag的值不为true，进入引导页
					uni.redirectTo({
						url: './guide'
					});
				}
			}
		}
	}
</script>
<style>
	
</style>
