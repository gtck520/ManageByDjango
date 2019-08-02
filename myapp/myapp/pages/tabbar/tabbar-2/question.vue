<template>
	<view class="content">
		<view class="padding">
			<button class="cu-btn block bg-blue margin-tb-sm lg" type="" @click="gotoTest">开始</button>
			<button class="cu-btn block line-blue margin-tb-sm lg" disabled>无效状态</button>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				title: 'Hello'
			}
		},
		onLoad() {

		},
		methods: {
			gotoTest(){
				uni.navigateTo({
					url:"../../question/catalogue"
				})
			}

		}
	}
</script>

<style>
	.content {
		text-align: center;
		height: 400upx;
		margin-top: 200upx;
	}
</style>
