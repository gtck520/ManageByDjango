<template>
	<view class="contenta" >		
	<cu-custom bgImage="../../../static/img/sylb2244.jpg" :isBack="true">
		<block slot="backText">返回</block>
		<block slot="content">分享</block>
	</cu-custom>
	<view class="top"></view>
	<view class="banner">
		<dl>
			<dt><image :src="userinfo.image" mode=""></image></dt>
			<dd>{{userinfo.mobile}}</dd>
		</dl>
		<view class="img">
			<view class="qrimg-i">
				<tki-qrcode v-if="ifShow" cid="qrcode1" ref="qrcode" :val="val" :size="size" :unit="unit" :icon="icon" :iconSize="iconsize" :lv="lv" :onval="onval" :loadMake="loadMake" :usingComponents="true" @result="qrR" />
			</view>
		</view>
		<view class="tgtit">推广链接：<text class="tugurl">{{val}}</text></view>
		<view class="sharbuttn">
			<view class="btn" @tap="saveQrcode">保存二维码</view>
			<view class="btn" @click="sharurl">复制推广链接</view>
		</view>
		
		<!-- <button class="btn" @click="share">分享</button> -->
		<view class="shartitle"><view>分享</view></view>
		<view class="sharapk" @click="share">
			<view><image src="../../../static/img/shar.png"></image></view>
			<view><image src="../../../static/img/qq.png"></image></view>
		</view>
		
		
		<view class="bottom">
			<ul>
				<li>1、好友识别二维码通过手机号进行注册</li>
				<li>2、也可分享此页面到微信或QQ邀请好友注册</li>
				<li>3、注册完成后您即可得到相应的积分</li>
			</ul>
		</view>
	</view>
	
	<!-- 二维码功能 -->
<!-- 		<view class="qrimg">
			<view class="qrimg-i">
				<tki-qrcode v-if="ifShow" cid="qrcode1" ref="qrcode" :val="val" :size="size" :unit="unit" :background="background" :foreground="foreground" :pdground="pdground" :icon="icon" :iconSize="iconsize" :lv="lv" :onval="onval" :loadMake="loadMake" :usingComponents="true" @result="qrR" />
			</view>
			<view class="qrimg-i">
				<tki-qrcode v-if="ifShow" cid="qrcode2" ref="qrcode2" val="第二个二维码" :size="size" :onval="onval" :loadMake="loadMake" :usingComponents="true" @result="qrR" />
			</view>
		</view>
		<view class="uni-padding-wrap">
			<view class="uni-title">请输入要生成的二维码内容</view>
		</view>
		<view class="uni-list">
			<input class="uni-input" placeholder="请输入要生成的二维码内容" v-model="val" />
		</view>
		<view class="uni-padding-wrap uni-common-mt">
			<view class="uni-title">设置二维码大小</view>
		</view>
		<view class="body-view">
			<slider :value="size" @change="sliderchange" min="50" max="500" show-value />
		</view>
		<view class="uni-padding-wrap">
			<view class="btns">
				<button type="primary" @tap="selectIcon">选择二维码图标</button>
				<button type="primary" @tap="creatQrcode">生成二维码</button>
				<button type="primary" @tap="saveQrcode">保存到图库</button>
				<button type="warn" @tap="clearQrcode">清除二维码</button>
				<button type="warn" @tap="ifQrcode">显示隐藏二维码</button>
			</view>
		</view> -->
	<!-- 二维码功能 -->
	
	</view>
</template>

<script>
import tkiQrcode from '@/components/tki-qrcode/tki-qrcode.vue'
	export default {
		data(){
			return {
				ifShow: true,
				val: '', // 要生成的二维码值
				size: 300, // 二维码大小
				unit: 'upx', // 单位
				background: '#b4e9e2', // 背景色
				foreground: '#309286', // 前景色
				pdground: '#32dbc6', // 角标色
				icon: '', // 二维码图标
				iconsize: 40, // 二维码图标大小
				lv: 3, // 二维码容错级别 ， 一般不用设置，默认就行
				onval: false, // val值变化时自动重新生成二维码
				loadMake: true, // 组件加载完成后自动生成二维码
				src: '' ,// 二维码生成后的图片地址或base64				
				providerList:[],				
				sourceLink: 'http://yunzhujiao.cn/bind_pub/index.html',		
				type:0,
				userinfo:''
			}
		},
		components: {
			tkiQrcode
		},
		onLoad(option) {
			this.userinfo = JSON.parse(option.m);
			this.val=this.$weburl+'#/pages/mine/children/register?re='+this.userinfo.id;
			this.creatQrcode();
			this.version = plus.runtime.version;
			uni.getProvider({
				service: 'share',
				success: (e) => {
					let data = [];
					for (let i = 0; i < e.provider.length; i++) {
						switch (e.provider[i]) {
							case 'weixin':
								data.push({
									name: '分享到微信好友',
									id: 'weixin'
								})
								data.push({
									name: '分享到微信朋友圈',
									id: 'weixin',
									type: 'WXSenceTimeline'
								})
								break;
							case 'qq':
								data.push({
									name: '分享到QQ',
									id: 'qq'
								})
								break;
							default:
								break;
						}
					}
					this.providerList = data;
				},
				fail: (e) => {
					console.log('获取登录通道失败'+ JSON.stringify(e));
				}
			});
		},
		methods:{
			
			//复制分享链接
			sharurl(){
				uni.setClipboardData({
					data: this.val,
					success: function () {
						console.log('success');
						// uni.showModal({
						// 	title: '复制成功',
						// 	content: '内容已复制到粘贴板，可前往其他应用粘贴查看。', 
						// 	showCancel:false,
						// 	success: function(res) {
						// 		if (res.confirm) {											 
						// 			//console.log('用户点击确定');
						// 		} else if (res.cancel) {
						// 			//console.log('用户点击取消');
						// 		}
						// 	}
						// });
					}
				});
			},
			//保存图片到相册
			save(){
				uni.showActionSheet({
					itemList:['保存图片到相册'],
					success: () => {
						plus.gallery.save('http://pds.jyt123.com/wxtest/logo.png', function() {
							uni.showToast({
								title:'保存成功',
								icon:'none'
							})
						}, function() {
							uni.showToast({
								title:'保存失败，请重试！',
								icon:'none'
							})
						});
					}
				})
			},
			share(e) {
				if (this.providerList.length === 0) {
					uni.showModal({
						title: '当前环境无分享渠道!',
						showCancel: false
					})
					return;
				}
				let itemList = this.providerList.map(function (value) {
					return value.name
				})
				 
				console.log(itemList)
				
				uni.showActionSheet({
					itemList: itemList,
					success: (res) => {
						console.log(this.providerList[res.tapIndex].id)
						if(this.providerList[res.tapIndex].id=='qq'){
							this.type=1
						}else{
							this.type=0
						}
						 uni.share({
						 	provider: this.providerList[res.tapIndex].id,
						 	scene: this.providerList[res.tapIndex].type && this.providerList[res.tapIndex].type === 'WXSenceTimeline' ? 'WXSenceTimeline' : "WXSceneSession",
						 	type: this.type,
						 	title:'耘助教',
						 	summary: '耘助教是一个在线教育应用平台',
						 	imageUrl:'http://pds.jyt123.com/wxtest/logo.png',
						 	href:"https://m3w.cn/uniapp",
						 	success: (res) => {
						 		console.log("success:" + JSON.stringify(res));
						 	},
						 	fail: (e) => {
						 		uni.showModal({
						 			content: e.errMsg,
						 			showCancel:false
						 		})
						 	}
						 });
					}
				})
				
				
				
			 
			},
			openLink() {
				plus.runtime.openWeb(this.sourceLink)
			},
			
			//二维码功能
			sliderchange(e) {
				this.size = e.detail.value
			},
			creatQrcode() {
				this.$refs.qrcode._makeCode()
			},
			saveQrcode() {
				this.$refs.qrcode._saveCode()
			},
			qrR(res) {
				this.src = res
			},
			clearQrcode() {
				this.$refs.qrcode._clearCode()
				this.val = ''
			},
			ifQrcode() {
				this.ifShow = !this.ifShow
			},
			selectIcon() {
				let that = this
				uni.chooseImage({
					count: 1, //默认9
					sizeType: ['original', 'compressed'], //可以指定是原图还是压缩图，默认二者都有
					sourceType: ['album'], //从相册选择
					success: function (res) {
						that.icon = res.tempFilePaths[0]
						setTimeout(() => {
							that.creatQrcode()
						}, 100);
						// console.log(res.tempFilePaths);
					}
				});
			}
		}
	}
	
	
</script>

<style>
	.tugurl{
		color: #999;
	}
	.sharbuttn{
		display: flex;
		justify-content: center;
	}
	.shartitle{
		    width: 80%;
			text-align: center;
			margin-left: 10%;
			border-bottom: 1px solid #dddddd;
			position: relative;
			height: 60upx;
	}
	.tgtit{
		text-align: center;
	}
	.shartitle view{
		    height: 50upx;
			line-height: 50upx;
			font-size: 28upx;
			color: #999;
			width: 120upx;
			margin: 32upx auto;
			position: absolute;
			background: #fff;
			left: 50%;
			margin-left: -60upx;
	}
	.sharapk{
	 display: flex;
	 justify-content: center;
	 margin: 20upx auto
	}
	.sharapk view{
		margin: 40upx;
	}
	.sharapk view image{
		height: 80upx;
		width: 80upx;
	}
	.contenta{
		width: 100%;
		background-color: #ffffff;
	}
	.top{
		width: 100%;
		height:400upx;
		background: url(http://pds.jyt123.com/wxtest/banner.png) no-repeat ;
		background-size:100% ;
		background-position:center center;
	}
	.banner{
		width: 100% ;
		background-color: #FFFFFF;
		border-radius: 60upx 60upx 0 0;
		margin-top: -60upx;
	}
	.banner dl{
		margin-top: -80upx;
	}
	.banner dl dt{
		text-align: center;
	}
	.banner dl dt image{
		width: 160upx;
		height: 160upx;
		border-radius:50% ;
	}
	.banner dl dd{
		text-align: center;
	}
	.img{
		width: 300upx;
		height: 300upx;
		background-color: red;
		margin: 0 auto;
		margin-top: 60upx;
	}
	.img image{
		width: 100%;
		height: 100%;
	}
	.btn{
		width: 260upx;
		height: 60upx;
		line-height: 60upx;
		margin: 0 auto;
		margin-top: 60upx;
		border-radius: 40upx;
		border: 0;
		font-size: 26upx;
		outline: 0;
		background: #33b17b;
		color: #FFFFFF;
		text-align: center;
	}
	.bottom{
		width: 100%;
		height: 400upx;
	/* 	background: url(../../static/img/beij.png) no-repeat; */
		background-position:left bottom;/* 设置背景图片位置 */
		background-size: 20%;
	}
	.bottom ul{
		padding-left: 40upx;
		box-sizing: border-box;
	}
	.bottom ul li{
		width: 100%;
		height: 60upx;
	}
</style>
