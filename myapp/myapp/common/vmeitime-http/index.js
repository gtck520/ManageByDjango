import http from './interface'

/**
 * 将业务所有接口统一起来便于维护
 * 如果项目很大可以将 url 独立成文件，接口分成不同的模块
 * 
 */

// 单独导出(测试接口) import {test} from '@/common/vmeitime-http/'
export const login = (data) => {
	/* http.config.baseUrl = "http://localhost:8080/api/"
	//设置请求前拦截器
	http.interceptor.request = (config) => {
		config.header = {
			"token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
		}
	} */
	//设置请求结束后拦截器
	http.interceptor.response = (response) => {
		console.log('个性化response....')
		//判断返回状态 执行相应操作
		return response;
	}
    return http.post('login/',data);
}
// 注册接口
export const register = (data) => {
    return http.post('v1/users/',data);
}
//验证接口登录状态
export const islogin = (data) => {
	if(data.detail=='Signature has expired.' || data.detail=='身份认证信息未提供。'){
		uni.showModal({
		title: '提示',
		content: '您还未登录或登录已过期，请登录',
		showCancel:false,
		success: function (res) {	
			uni.navigateTo({
				url:"../basiclogin/login?isback=1"
			});
		}
		});
		return false;
	}
	else{
		return true;
	}
}
//判断返回数据是否请求成功
export const isSuccess = (statusCode) => {
	if(statusCode===200 || statusCode===201 ||statusCode===204){
		return true;
	}
	else{
		return false;
	}
}

// 读取用户信息
export const getGlobalUser = (data) => {
    return http.get('v1/userinfo/',data);
}

// 获取验证码
export const getCaptcha = (data) => {
    return http.get('v1/captchas/',data);
}

// 检验验证码
export const checkCaptchas = (data) => {
    return http.post('v1/captchas/check/',data);
}

// 发送手机验证码
export const sendCode = (data) => {
    return http.post('v1/codes/',data);
}

// 获取圣经卷名列表
export const getVolume = (data) => {
    return http.get('v1/books/',data);
}

// 获取圣经章列表
export const getChapters = (booksn,data) => {
    return http.get('v1/books/'+booksn+'/chapters/',data);
}

// 获取圣经节列表
export const getVerses = (booksn,chaptersn,data) => {
    return http.get('v1/books/'+booksn+'/chapters/'+chaptersn+'/',data);
}

// 获取圣经内容
export const getcontents = (booksn,chaptersn,data) => {
    return http.get('v1/contents/'+booksn+'/'+chaptersn+'/',data);
}

// 查找圣经内容
export const getSearch = (searchstr,page,data) => {
    return http.get('v1/contents/search/'+searchstr+'/?page='+page,data);
}

// 获取新闻分类
export const loadTabbars = (data) => {
    return http.get('v1/newsclass/',data);
}

// 获取新闻列表
export const loadNewsList = (data) => {
    return http.get('v1/news/',data);
}

// 获取新闻详细信息
export const getNewDetail = (newid,data) => {
    return http.get('v1/news/'+newid+'/',data);
}

// 获取新闻评论列表
export const getNewComment = (newid,data) => {
    return http.get('v1/comments/?type=1&news='+newid,data);
}

// 提交评论信息
export const subcomment = (data) => {
    return http.post('v1/comments/',data);
}

// 获取用户对所选新闻的收藏信息
export const getfavorite = (newid,data) => {
    return http.get('v1/favorite/?news='+newid,data);
}

// 收藏、取消收藏
export const setfavorite = (status,data,deleteid) => {
	if (!deleteid) {
		deleteid = 0;
	}
	if(status==false){
		//未收藏则执行收藏
		return http.post('v1/favorite/',data);
	}else{
		//已收藏则删除收藏
		return http.delete('v1/favorite/'+deleteid+'/',data);
	}
   
}

// 获取用户对所选新闻的点赞信息
export const getsnap = (newid,type,data) => {
    return http.get('v1/snap/?news='+newid+'&type='+type,data);
}

// 点赞、取消点赞
export const setsnap = (status,data,deleteid) => {
	if (!deleteid) {
		deleteid = 0;
	}
	if(status==false){
		//未收藏则执行收藏
		return http.post('v1/snap/',data);
	}else{
		//已收藏则删除收藏
		return http.delete('v1/snap/'+deleteid+'/',data);
	}
   
}
// 默认全部导出  import api from '@/common/vmeitime-http/'
export default {
	isSuccess,
	login,
	islogin,
    register,
	getCaptcha,
	checkCaptchas,
	sendCode,
	getVolume,
	getChapters,
	getVerses,
	getcontents,
	getSearch,
	loadTabbars,
	loadNewsList,
	getNewDetail,
	getNewComment,
	subcomment,
	getfavorite,
	setfavorite,
	getGlobalUser,
	getsnap,
	setsnap
}