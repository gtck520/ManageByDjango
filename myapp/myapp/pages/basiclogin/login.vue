<template>
	<view class="content">
		<view class="logo"><image src="../../static/basiclogin/logo.png" mode=""></image></view>
		<view class="uni-form-item uni-column">
			<input type="tel" class="uni-input"  v-model="name" placeholder="请输入手机号" />
		</view>
		<view class="uni-form-item uni-column">
			<input type="password" class="uni-input" v-model="pass" placeholder="请输入密码" />
		</view>
		<button type="primary" @tap="login">登陆</button>
		<view class="links"><view @tap="gotoForgetPassword">忘记密码？</view><view>|</view><view class="link-highlight" @tap="gotoRegistration">注册账号</view></view>
		
		<view class="cu-modal" :class="modalName=='Modal'?'show':''">
			<view class="cu-dialog">
				<view class="cu-bar bg-white justify-end">
					<view class="content">提示</view>
					<view class="action" @tap="hideModal">
						<text class="cuIcon-close text-red"></text>
					</view>
				</view>
				<view class="padding-xl">
					{{modalcontent}}
				</view>
			</view>
		</view>
	</view>
</template>

<script>
	export default {
		data() {
			return {
				name : '',
				pass : '',
				modalName: null,
				modalcontent:'',
				isback:0
			};
		},
		onLoad(option) {
			this.isback=option.isback;//判断登录完成是否返回上一个页面
		},
		methods: {
			login(e) {
				var url = 'login/';
				this.urlRequest({
				url: url,
				data: {
					username : this.name,
					password : this.pass
				},
				method: 'POST',
				success: res => {
					console.log(res);
					if (res.statusCode == 200) {
						var token = res.data.token;
						// 保存用户token
						uni.setStorageSync("token", token);
						if(this.isback==1)
						{
							uni.navigateBack();
						}else{
							// 切换页面跳转，使用tab切换的api
							uni.switchTab({
								url: "../tabbar/tabbar-5/my",
								// success() {
								// 	
								// }
							});
						}
						
					}
					else if(res.statusCode == 400){
						var msg = '账号或密码错误，请重新输入';
						this.showModal(msg);
					}
				},
				fail: () => {},
				complete: () => {}
				});
			},
			showModal(msg) {
				this.modalName = 'Modal';
				console.log(this.modalName);
				this.modalcontent = msg;
			},
			hideModal(e) {
				this.modalName = null
			},
			gotoRegistration: function () {
				uni.navigateTo({url: 'registration'});
			},
			gotoForgetPassword: function () {
				uni.navigateTo({url: 'forget-password'});
			}
		}
	}
</script>

<style lang="scss" scoped>
	$color-primary: #b49950;
	.content{
		padding: 100upx;
	}
	.logo{
	    text-align: center;
		image{
		    height: 200upx;
		    width: 200upx;
		    margin: 0 0 60upx;
		}
	}
	.uni-form-item{
		margin-bottom: 40upx;
		padding: 0;
		border-bottom: 1px solid #e3e3e3;
		.uni-input{
			font-size: 30upx;
			padding: 7px 0;
		}
	}
	button[type="primary"]{
		background-color: $color-primary;
		border-radius: 0;
		font-size: 34upx;
		margin-top: 60upx;
	}
	.links{
		text-align: center;
		margin-top: 40upx;
		font-size: 26upx;
		color: #999;
		view{
			display: inline-block;
			vertical-align: top;
			margin: 0 10upx;
		}
		.link-highlight{
			color: $color-primary
		}
	}
</style>
