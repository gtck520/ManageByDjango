<template>
	<view class="content">
		<view>{{title}}</view>
		<view style="width: 660upx;text-align: center;color: #918984;">清除launchFlag值进行测试，H5端不会刷新，请手动刷新，APP端会重启APP。</view>
		<view class="out-btn" @tap="outBtn()">清除launchFlag值</view>
	</view>
</template>

<script>
export default {
	data() {
		return {
			title: 'Hello'
		};
	},
	onLoad() {},
	methods: {
		outBtn: function(){
			// 清除缓存
			uni.clearStorage();
			// 两秒后重启
			setTimeout(function() {
				plus.runtime.restart();
			}, 2000);
		}
	}
};
</script>

<style>
.content {
	text-align: center;
	height: 400upx;
	margin-top: 200upx;
}
.out-btn{
	width: 660upx;
	height: 80upx;
	margin: 0 auto;
	text-align: center;
	line-height: 80upx;
	background: #918984;
	color: #FFFFFF;
	border-radius: 40upx;
}
</style>
