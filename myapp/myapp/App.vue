<script>
	import Vue from 'vue'
	
	export default {
		created() {
			// #ifdef APP-PLUS
			plus.navigator.closeSplashscreen(); 
			// #endif 
		},
		onLaunch: function() {
			
			console.log('App Launch')
			uni.getSystemInfo({
				success: function(e) {
					// #ifndef MP
					Vue.prototype.StatusBar = e.statusBarHeight;
					if (e.platform == 'android') {
						Vue.prototype.CustomBar = e.statusBarHeight + 50;
					} else {
						Vue.prototype.CustomBar = e.statusBarHeight + 45;
					};
					// #endif
		
					// #ifdef MP-WEIXIN
					Vue.prototype.StatusBar = e.statusBarHeight;
					let custom = wx.getMenuButtonBoundingClientRect();
					Vue.prototype.Custom = custom;
					Vue.prototype.CustomBar = custom.bottom + custom.top - e.statusBarHeight;
					// #endif		
		
					// #ifdef MP-ALIPAY
					Vue.prototype.StatusBar = e.statusBarHeight;
					Vue.prototype.CustomBar = e.statusBarHeight + e.titleBarHeight;
					// #endif
				}
			})
		},
		onShow: function() {
			console.log('App 开启')
		},
		onHide: function() {
			console.log('App 关闭')
		}
	}
</script>

<style lang="less">
	/*每个页面公共css */
	@import url("./style/animation/animation.css"); /* 动画 */
	@import "colorui/main.css";
	@import "colorui/icon.css";
	
	/* 加载loding */
	.cu-load.load-modal {
		width: 0px;
		height: 0px;
		background-color: transparent;
	}
	.cu-load.load-modal::after {
		background-color: rgba(0, 0, 0, 0.3);
		width: 30px;
		height: 30px;
		border-left: 3px solid #FFF0F6;
	}
	body{
		background: #FFFFFF !important;
	}
	/* 阴影 */
	.bar-shadown{
		-webkit-box-shadow: 0 0 36px 0 rgba(43,86,112,.1) !important;
		box-shadow: 0 0 36px 0 rgba(43,86,112,.1) !important;
	}
	/* mixnews */
		@font-face {
		font-family: yticon;
		font-weight: normal;
		font-style: normal;
		src: url('https://at.alicdn.com/t/font_1078604_3mrhac2o3oi.ttf') format('truetype');
	}
	
	.yticon {
		font-family: "yticon" !important;
		font-size: 16px;
		font-style: normal;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
	}
	.icon-shoucang:before {
		content: "\e645";
	}
	.icon-shoucang_xuanzhongzhuangtai:before {
		content: "\e6a9";
	}
	.icon-dianzan-ash:before {
	  content: "\e617";
	}
	.icon-fenxiang2:before {
		content: "\e61e";
	}
</style>
