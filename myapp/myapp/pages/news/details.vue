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
						<view class="action-item" @click="setsnap" data-typeid='1'>
							<text class="yticon icon-dianzan-ash " :class="mysnap==true?'active':''"></text>
							<text >{{snap_nums}}</text>
						</view>
<!-- 						<view class="action-item">
							<text class="yticon icon-dianzan-ash reverse"></text>
							<text>6</text>
						</view> -->
						<view class="action-item" @click="setfavorite">
							<text class="yticon icon-shoucang " :class="myfav==true?'active':''"></text>
							<text >收藏</text>
						</view>
						<view class="action-item">
							<text class="yticon icon-fenxiang2"></text>
							<text >分享</text>
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
					<scroll-view class="uni-comment" scroll-y scroll-with-animation :scroll-into-view="'main-'+nowcomment">
						<view class="uni-comment-list" v-for="(item,index) in commentList" :key="index" :id="'main-'+item.id">
							<view class="uni-comment-face">
								<image :src="item.user.image" mode="widthFix"></image>
							</view>
							<view class="uni-comment-body">
								<view class="uni-comment-top">
									<text>{{item.user.nick_strname}}</text>
									<view class="cuIcon-appreciate " :style="item.snapid>0?'color: #ec706b;':''" v-if="item.snap_nums>0" @click="setsnap" data-typeid='2' :data-snapid='item.snapid' :data-comentid='item.id'>{{item.snap_nums}}</view>
									<view class="cuIcon-appreciate " v-else @click="setsnap" data-typeid='2' :data-snapid='item.snapid' :data-comentid='item.id'>赞</view>									
								</view>
								<view class="uni-comment-content">{{item.comments}}</view>
								<view class="uni-comment-date">
									<view>{{item.add_time}}</view>
									<view class="uni-comment-replay-btn" v-if="item.comentslist.count >0 ">{{item.comentslist.count}} 回复</view>
									<view class="uni-comment-replay-btn" v-else>回复</view>
								</view>
							</view>
						</view>
					</scroll-view>
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
				nowcomment:'',
				mycomment:'',
				myfav:false,//是否收藏当前文章
				deleteid:0,//收藏id
				snap_nums:0,
				mysnap:false,//是否点赞当前文章
				deletesnap:0,//点赞id
			}
		},
		onLoad(options){
			this.detailData = JSON.parse(options.data);
			this.getNewDetail();
			this.getNewComment();
			this.loadNewsList();
			this.loadEvaList();
			this.getfavorite();
			this.getsnap();
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
			async getNewDetail(){
				//此处为封装请求之异步用法
                this.loading = true
                let res = await this.$api.getNewDetail(this.detailData.id,{noncestr: Date.now()});
                this.loading = false;
				this.detailData = res.data;
				this.snap_nums = res.data.snap_nums;
			},
			//获取评论列表
			getNewComment(){
				// 获取评论列表
				this.loading = true
				this.$api.getNewComment(this.detailData.id,{noncestr: Date.now()}).then((res)=>{
					this.loading = false;
					this.commentList = res.data.results;
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});		
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
									
				this.loading = true;
				this.$api.subcomment({
						'comment_id':comment_id,
						'comment_type':comment_type,
						'comments':this.mycomment,
					}).then((res)=>{
					this.loading = false;
					if (res.statusCode == 201) {
							this.mycomment='';
							let userinfo=uni.getStorageSync('userinfo');
							let item = res.data;
							let user ={
								'nick_strname':userinfo.nick_strname,
								'image':userinfo.image
							}
							let comentslist={
								'count':0
							}
							item.user = user;
							item.comentslist=comentslist;
							this.commentList.push(item);
							this.nowversesn='main'+res.data.id;							
						
					}else{
						this.$api.islogin(res.data);					
					}
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});		
			},
			//获取对当前文章的收藏信息
			getfavorite(){
				this.$api.getfavorite(this.detailData.id,{}).then((res)=>{					
					this.loading = false;
					if(res.data.id>0)
					{	
						this.myfav=true;
						this.deleteid=res.data.id;
					}				
				}).catch((err)=>{
					this.loading = false;
					console.log(err);
				});	
				
			},
			//收藏与取消
			setfavorite(){				
				this.loading = true
				if(this.myfav==false){
					var data={
					'fav_id':this.detailData.id,
					'fav_type':1,
					};
				}
				else{
					var data={};
				}
				this.$api.setfavorite(this.myfav,data,this.deleteid).then((res)=>{
					this.loading = false;					
					if(this.$api.islogin(res.data)){
						this.myfav=!this.myfav;
						this.deleteid=res.data.id;
					}
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});				
			},
			//获取对当前文章的点赞信息
			getsnap(){
				this.$api.getsnap(this.detailData.id,1,{}).then((res)=>{
				this.loading = false;						
				if(res.data.id>0)
				{	
					this.mysnap=true;
					this.deletesnap=res.data.id;
				}			
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
				});	
				
			},
			//点赞与取消
			setsnap(e){			
				var type=e.currentTarget.dataset.typeid;
				var sid=0;
				var issnap=false;
				var deletesnap=0;
				if(type==1){
					sid=this.detailData.id;
					issnap=this.mysnap;
					deletesnap=this.deletesnap
				}else{
					sid=e.currentTarget.dataset.comentid;
					issnap=e.currentTarget.dataset.snapid>0?true:false;	
					deletesnap=e.currentTarget.dataset.snapid;
				}
				 
				this.loading = true
				if(issnap==false){
					var data={
					'snap_id':sid,
					'snap_type':type,
					};
				}
				else{
					var data={};
				}
				this.$api.setsnap(issnap,data,deletesnap).then((res)=>{
					this.loading = false;		
					if(this.$api.islogin(res.data)){
						if(type==1){
							this.mysnap=!issnap;
							this.deletesnap=res.data.id;
							if(this.mysnap){
								this.snap_nums=this.snap_nums+1;
							}else{
								this.snap_nums=this.snap_nums-1;
							}
						}else{
							this.getNewComment();
						}
						
						
					}
				}).catch((err)=>{
					this.loading = false;
					console.log('request fail', err);
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
