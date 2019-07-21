<template>
	<view class="content">
	
		<scroll-view class="scroll" scroll-y>
			<view class="scroll-content">
				<view class="introduce-section">
					<text class="title">{{detailData.title}}</text>
					<view class="introduce">
						<text>{{detailData.authorname}}</text>
						<text>{{detailData.click_nums}}阅读</text>
						<text>{{detailData.add_time}}</text>
					</view>
					
					<rich-text :nodes="detailData.detail"></rich-text>
					
					<view class="actions" v-show="loading === false">
						<view class="action-item">
							<text class="yticon icon-dianzan-ash"></text>
							<text class="cuIcon-appreciate" >75</text>
						</view>
<!-- 						<view class="action-item">
							<text class="yticon icon-dianzan-ash reverse"></text>
							<text>6</text>
						</view> -->
						<view class="action-item">
							<text class="yticon icon-shoucang active"></text>
							<text class="cuIcon-favor" >收藏</text>
						</view>
						<view class="action-item">
							<text class="yticon icon-fenxiang2"></text>
							<text class="cuIcon-share">分享</text>
						</view>
					</view>
				</view>
				
				<view class="container" v-show="loading === false">
					<!-- 推荐 -->
					<view class="s-header">
						<text class="tit">相关推荐</text>
					</view>
					<view class="rec-section" v-for="item in newsList" :key="item.id">
						<view class="rec-item">
							<view class="left">
								<text class="title">{{item.title}}</text>
								<view class="bot">
									<text class="author">{{item.author}}</text>
									<text class="time">{{item.time}}</text>
								</view>
							</view>
							<view class="right" v-if="item.images.length > 0">
								<image class="img" :src="item.images[0]" mode="aspectFill"></image>
							</view>
						</view>
					</view>
					
					<!-- 评论 -->
				<view class="uni-padding-wrap">
					<!-- 评论区 start -->
					<view class="uni-comment">
						<view class="uni-comment-list" v-for="(item,index) in commentList" :key="index">
							<view class="uni-comment-face">
								<image :src="item.user.image" mode="widthFix"></image>
							</view>
							<view class="uni-comment-body">
								<view class="uni-comment-top">
									<text>{{item.user.nick_strname}}</text>
									<view class="cuIcon-appreciate">{{item.snap_nums}}</view>									
								</view>
								<view class="uni-comment-content">{{item.comments}}</view>
								<view class="uni-comment-date">
									<view>2天前</view>
									<view class="uni-comment-replay-btn">5回复</view>
								</view>
							</view>
						</view>
					</view>
				</view>
				</view>
				<!-- 加载图标 -->
				<mixLoading class="mix-loading" v-if="loading"></mixLoading>
			</view>
		</scroll-view>
		
		<view class="bottom">
			<view class="input-box">
				<text class="yticon icon-huifu"></text>
				<input 
					class="input"
					type="text" 
					placeholder="点评一下把.." 
					placeholder-style="color:#adb1b9;"
					v-model="mycomment"
				/>
			</view>
			<text class="confirm-btn" @tap="subcomment">提交</text>
		</view>
	</view>
</template>

<script>
	import json from '@/json';
	import mixLoading from '@/components/mix-loading/mix-loading';
	export default {
		components: {
			mixLoading
		},
		data() {
			return {
				loading: true,
				detailData: {},
				newsList: [],
				evaList: [],
				commentList:[],
				mycomment:''
			}
		},
		onLoad(options){
			this.detailData = JSON.parse(options.data);
			this.getNewDetail();
			this.getNewComment();
			this.loadNewsList();
			this.loadEvaList();
		},
		methods: {
			//获取推荐列表
			async loadNewsList(){
				let list = await json.newsList;
				setTimeout(()=>{
					list.sort((a,b)=>{
						return Math.random() > .5 ? -1 : 1; //静态数据打乱顺序
					})
					list.length = 5;
					list.forEach(item=>{
						this.newsList.push(item);
					});					
					this.loading = false;
				}, 1000)
			},
			//获取评论列表
			async loadEvaList(){
				this.evaList = await json.evaList;
			},
			//获取新闻详细
			getNewDetail(){
				// 获取新闻列表
				uni.request({
				url: this.ApiHost+'v1/news/'+this.detailData.id+'/',
				data: {},
				method: 'GET',
				}) .then(data => {
					var [error, res]  = data;
					this.detailData = res.data;
					this.loading = false;
				})
			},
			//获取评论列表
			getNewComment(){
				// 获取新闻列表
				uni.request({
				url: this.ApiHost+'v1/comments/?news='+this.detailData.id,
				data: {},
				method: 'GET',
				}) .then(data => {
					var [error, res]  = data;
					this.commentList = res.data.results;
				})
			},
			//提交评论
			subcomment(){
				if(this.mycomment==''){
					uni.showModal({
						title: '提示',
						content: '评论内容不能为空',
						showCancel:false,
						success: function (res) {
							
						}
					});
					return false;
				}
				var comment_id=this.detailData.id;
				var comment_type=1;
				this.urlRequest({
					url: 'v1/comments/',
					data: {
						'comment_id':comment_id,
						'comment_type':comment_type,
						'comments':this.mycomment,
					},
					method: 'POST',
					success: res => {
						if (res.statusCode == 200) {
							
							
						}else{
							if(res.data.user=='该字段是必填项。'||res.data.detail=='身份认证信息未提供。'){
								uni.showModal({
								title: '提示',
								content: '您还未登录，请先登录',
								showCancel:false,
								success: function (res) {	
									uni.navigateTo({
										url:"../basiclogin/login?isback=1"
									});
								}
								});
							}
							else{
								console.log(res.data);
							}
							
						}
					},
					fail: () => {},
					complete: () => {}
				});
			}
			
		}
	}
</script>

<style lang="scss">
	page{
		height: 100%;
	}
	.content{
		display: flex;
		flex-direction: column;
		height: 100%;
		background: #fff;
	}
	.video-wrapper{
		height: 422upx;
		
		.video{
			width: 100%;
			height: 100%;
		}
	}
	.scroll{
		flex: 1;
		position: relative;
		background-color: #f8f8f8;
		height: 0;
	}
	.scroll-content{
		display: flex;
		flex-direction: column;
	}
	/* 简介 */
	.introduce-section{
		display: flex;
		flex-direction: column;
		padding: 20upx 30upx;
		background: #fff;
		line-height: 1.5;
		
		.title{
			font-size: 36upx;
			color: #303133;
			margin-bottom: 16upx;
		}
		.introduce{
			display: flex;
			font-size: 26upx;
			color: #909399;
			text{
				margin-right: 16upx;
			}
		}
	}
	/* 点赞等操作 */
	.actions{
		display: flex;
		justify-content: space-around;
		align-items: center;
		line-height: 1.3;
		padding: 10upx 40upx 20upx;
	
		.action-item{
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
			font-size: 24upx;
			color: #999;
		}
		.yticon{
			display: flex;
			align-items: center;
			justify-content: center;
			width: 60upx;
			height: 60upx;
			font-size: 52upx;
			
			&.reverse{
				position: relative;
				top: 6upx;
				transform: scaleY(-1);
			}
			&.active{
				color: #ec706b;
			}
		}
		.icon-fenxiang2{
			font-weight: bold;
			font-size: 36upx;
		}
		.icon-shoucang{
			font-size: 44upx;
		}
	}

	.s-header{
		padding: 20upx 30upx;
		font-size: 30upx;
		color: #303133;
		background: #fff;
		margin-top: 16upx;
		
		&:before{
			content: '';
			width: 0;
			height: 40upx;
			margin-right: 24upx;
			border-left: 6upx solid #ec706b;
		}
	}
	/* 推荐列表 */
	.rec-section{
		background-color: #fff;
		.rec-item{
			display: flex;
			padding: 20upx 30upx;
			position: relative;
			&:after{
				content: '';
				position: absolute;
				left: 30upx;
				right: 0;
				bottom: 0;
				height: 0;
				border-bottom: 1px solid #eee;
				transform: scaleY(50%);
			}
		}
		.left{
			flex: 1;
			padding-right: 10upx;
			overflow: hidden;
			position: relative;
			padding-bottom: 52upx;
			.title{
				display: -webkit-box;
				-webkit-box-orient: vertical;
				-webkit-line-clamp: 2;
				overflow: hidden;
				font-size: 32upx;
				color: #303133;
				line-height: 44upx;
			}
			.bot{
				position: absolute;
				left: 0;
				bottom: 4upx;
				font-size: 26upx;
				color: #909399;
			}
			.time{
				margin-left: 20upx;
			}
		}
		.right{
			width: 220upx;
			height: 140upx;
			flex-shrink: 0;
			position: relative;
			.img{
				width: 100%;
				height: 100%;
			}
			
		}
	}
	/* 评论 */
    .uni-padding-wrap {
        padding: 30upx;
		background: #fff;
    }

    view {
        font-size: 28upx;
    }

    .uni-comment {
        padding: 5rpx 0;
        display: flex;
        flex-grow: 1;
        flex-direction: column;
    }

    .uni-comment-list {
        flex-wrap: nowrap;
        padding: 10rpx 0;
        margin: 10rpx 0;
        width: 100%;
        display: flex;
    }

    .uni-comment-face {
        width: 70upx;
        height: 70upx;
        border-radius: 100%;
        margin-right: 20upx;
        flex-shrink: 0;
        overflow: hidden;
    }

    .uni-comment-face image {
        width: 100%;
        border-radius: 100%;
    }

    .uni-comment-body {
        width: 100%;
    }

    .uni-comment-top {
        flex-direction: row;
        justify-content: space-between;
        display: flex !important;
        line-height: 1.5em;
    }

    .uni-comment-top text {
        color: #0A98D5;
        font-size: 24upx;
    }

    .uni-comment-date {
        line-height: 38upx;
        flex-direction: row;
        justify-content: space-between;
        display: flex !important;
        flex-grow: 1;
    }

    .uni-comment-date view {
        color: #666666;
        font-size: 24upx;
        line-height: 38upx;
    }

    .uni-comment-content {
        line-height: 1.6em;
        font-size: 28upx;
        padding: 8rpx 0;
    }

    .uni-comment-replay-btn {
        background: #f2f3f3;
        font-size: 24upx;
        line-height: 28upx;
        padding: 5rpx 20upx;
        border-radius: 30upx;
        color: #333 !important;
        margin: 0 10upx;
    }
	
	/* 底部 */
	.bottom{
		flex-shrink: 0;
		display: flex;
		align-items: center;
		height: 90upx;
		padding: 0 30upx;
		box-shadow: 0 -1px 3px rgba(0,0,0,.04); 
		position: relative;
		z-index: 1;
		
		.input-box{
			display: flex;
			align-items: center;
			flex: 1;
			height: 60upx;
			background: #f2f3f3;
			border-radius: 100px;
			padding-left: 30upx;
			
			.icon-huifu{
				font-size: 28upx;
				color: #909399;
			}
			.input{
				padding: 0 20upx;
				font-size: 28upx;
				color: #303133;
			}
		}
		.confirm-btn{
			font-size: 30upx;
			padding-left: 20upx;
			color: #0d9fff;
		}
	}
</style>
