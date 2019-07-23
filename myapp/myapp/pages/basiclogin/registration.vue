<template>
	<view class="content">
		<view class="logo"><image src="../../static/basiclogin/logo.png" mode=""></image></view>
		<view class="uni-form-item uni-column">
			<input type="tel" class="uni-input" name="" placeholder="请输入手机号" v-model="mobile"/>
		</view>
		<view class="uni-form-item uni-column column-with-btn">
			<input type="text" class="uni-input" name="captchaCode" placeholder="请输入图片验证码" v-model="captchaCode" />
			<image :src="captchaImg"  class="img-captcha" @tap="changeimg"  :data="hashkey"></image>
		</view>
		<view class="uni-form-item uni-column column-with-btn">
			<input type="number" class="uni-input" name="" placeholder="请输入验证码" v-model="mobilecode"/>
			<button :class="{active : !disableCodeBtn}" :disabled="disableCodeBtn" @tap="sendCode">{{codeBtn.text}}</button>
		</view>
		<view class="uni-form-item uni-column">
			<input type="password" class="uni-input" name="" placeholder="请输入密码" v-model="password"/>
		</view>
		<button type="primary" @tap="register">注册</button>
		<view class="links">已有账号？<view class="link-highlight" @tap="gotoLogin">点此登陆</view></view>
		
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
				mobile:'',
				password:'',
				mobilecode:'',
				captchaCode: '',
				captchaImg: '',
				hashkey:'',
				seconds: 10,
				codeBtn: {
					text: '获取验证码',
					waitingCode: false,
					count: this.seconds
				},
				modalName: null,
				modalcontent:'',
				loading:false
			}
		},
		onLoad() {

		},
		onShow(){
			this.changeimg();
		},
		methods: {
			sendCode: function () {				
				//校验图片验证码				
				this.$api.checkCaptchas({
					hashkey:this.hashkey,
					imagecode:this.captchaCode
				}).then((res)=>{
					if (res.statusCode == 200) {
						if(res.data.status==true){
							 this.$api.sendCode({
								mobile:this.mobile,
							}).then((resb)=>{
								console.log('aaaa')
								console.log(resb)
								if(resb.statusCode == 201){			
									
									this.codeBtn.waitingCode = true;
									this.codeBtn.count = this.seconds;
									this.codeBtn.text = this.codeBtn.count + 's';
									
									let countdown = setInterval( () => {
										this.codeBtn.count--;
										this.codeBtn.text = this.codeBtn.count + 's';
										if( this.codeBtn.count < 0 ){
											clearInterval(countdown);
											this.codeBtn.text = '重新发送';
											this.codeBtn.waitingCode = false;
										}
									},1000);
								}else{				
									console.log(resb);
									this.showModal(resb.data.mobile);
								}								
							}).catch((err)=>{
								console.log('request fail', err);
								this.showModal('手机码发送失败');
							})						
						}else{
							this.showModal('图片验证码错误');
						}
					}else{
						this.showModal('图片验证码错误');
					}
				}).catch((err)=>{
				    console.log('request fail', err);
				});			

			},
			changeimg:function(){
				//获取图片验证码
				this.loading = true;
				 this.$api.getCaptcha().then((res)=>{
                    this.loading = false;
					if (res.statusCode == 200) {
						this.captchaImg = res.data.image_url;
						this.hashkey = res.data.hashkey;
					}
					else{
					}
                }).catch((err)=>{
                    this.loading = false;
                    console.log('request fail', err);
                });				

			},			
			gotoLogin: function () {
				uni.navigateTo({
					url: 'login'
				})
			},
			register(e){
				// 注册
				this.$api.register({
					username :this.mobile,
					code :this.mobilecode,
					mobile:this.mobile,
					password:this.password
				}).then((res)=>{
                    this.loading = false;
					var token = res.data.token;
					// 保存用户token
					uni.setStorageSync("token", token);
					// 切换页面跳转，使用tab切换的api
					uni.switchTab({
						url: "../tabbar/tabbar-5/my",
						// success() {
						// 	
						// }
					});
                }).catch((err)=>{
                    this.loading = false;
                    console.log('request fail', err);
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
		},
		computed: {
			disableCodeBtn: function (){
				return this.codeBtn.waitingCode || this.captchaCode.length < 4 || this.mobile.length< 11;
			} 
		}
	}
</script>

<style lang="scss" scoped>
	$color-primary: #b49950;
	.content{
		padding: 60upx 100upx 100upx;
	}
	.logo{
	    text-align: center;
		image{
		    height: 200upx;
		    width: 200upx;
		    margin: 0 0 40upx;
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
	.column-with-btn{
		display: flex;
		flex-direction: row;
		justify-content: space-between;
		align-items: center;
		button{
			font-size: 24upx;
			margin: 0;
			width: 180upx;
			text-align: center;
			&:after{
				border: none
			}
			&.active{
				background-color: $color-primary;
				color: $uni-text-color-inverse;
			}
		}
	}
	.img-captcha{
		width: 150upx;
		height: 60upx;
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
