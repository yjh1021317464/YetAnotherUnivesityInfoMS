<template>
  <div class="index">
    <!-- <div style="height: 60px">
      <span class='font'>欢迎进入本校教师信息管理模块</span>
      <p class='text'>教师是核心，是学校培养学生的人才，管理教师信息，了解教师需求很关键</p>
    </div>-->
    <el-row style="margin: 0 auto;">
      <!--<p class="font">以下是您的个人信息</p>-->
      <div class="searchbox" style="display: inline-block; float: right;"></div>
    </el-row>

    <el-table :data="tableData" stripe style="width: 100%">
      <el-table-column label="工号" prop="id"></el-table-column>
      <el-table-column label="入职年月" prop="enroll_date"></el-table-column>
      <el-table-column label="电子邮箱" prop="email"></el-table-column>
      <el-table-column label="专业代码" prop="major_id"></el-table-column>
      <el-table-column label="专业名称" prop="major_name"></el-table-column>
      <el-table-column label="职称">
          <template slot-scope="scope">
                <i v-if="scope.row.title===0">教授</i>
                <i v-else>副教授</i>
            </template>
	      </el-table-column>
      <el-table-column label="身份证件号" prop="person_id"></el-table-column>
      <el-table-column label="身份证件类型">
          <template slot-scope="scope">
                <i v-if="scope.row.person_id_type===0">身份证</i>
                <i v-else>护照</i>
            </template>
	      </el-table-column>
      <el-table-column label="中文名称" prop="person_name"></el-table-column>
      <el-table-column label="性别">
          <template slot-scope="scope">
                <i v-if="scope.row.gender===0">男</i>
                <i v-else>女</i>
            </template>
	      </el-table-column>
      <el-table-column label="出生日期" prop="birth"></el-table-column>
      <el-table-column label="国籍" prop="country"></el-table-column>
      <el-table-column label="家庭住址" prop="family_address"></el-table-column>
      <el-table-column label="家庭邮政编码" prop="family_zipcode"></el-table-column>
      <el-table-column label="家庭电话" prop="family_tel"></el-table-column>
      <el-table-column label="操作">
        <template slot-scope="scope">
          <el-button type="primary" @click="editData(scope.$index)">修改</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog title="填写你的修改信息" :visible.sync="dialogFormVisible" style="height: 100%">
      <el-form :model="form" :rules="rules" ref="form">
        <el-form-item label="电子邮箱" prop="email">
          <el-input v-model="form.email" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="身份证件类型" prop="person_id_type">
          <el-select v-model="form.person_id_type" placeholder="请选择身份证件类型">
            <el-option style="height: 80%" label="身份证" value="0" autocomplete="off"></el-option>
            <el-option style="height: 80%" label="护照" value="1" autocomplete="off"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="中文名称">
          <el-input autocomplete="off" v-model="form.person_name"></el-input>
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-select v-model="form.gender" placeholder="请选择性别">
            <el-option style="height: 80%" label="男" value="0" autocomplete="off"></el-option>
            <el-option style="height: 80%" label="女" value="1" autocomplete="off"></el-option>
            <!--<el-option style='height: 80%' label="保密" value="保密" autocomplete="off"></el-option>-->
          </el-select>
        </el-form-item>
        <el-form-item label="出生日期" prop="birth">
          <el-input autocomplete="off" v-model="form.birth"></el-input>
        </el-form-item>
        <el-form-item label="国籍" prop="country">
          <el-input autocomplete="off" v-model="form.country"></el-input>
        </el-form-item>
        <el-form-item label="家庭住址" prop="family_address">
          <el-input autocomplete="off" v-model="form.family_address"></el-input>
        </el-form-item>
        <el-form-item label="家庭邮政编码" prop="family_zipcode">
          <el-input autocomplete="off" v-model="form.family_zipcode"></el-input>
        </el-form-item>
        <el-form-item label="家庭电话">
          <el-input v-model="form.family_tel" autocomplete="off"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitFrom">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<style lang='scss'>
@import "../../static/css/base.scss";
.font {
  @include fontTwo();
}
.text {
  @include fontThree();
}
.el-dialog__body {
  padding: 10px 20px;
}
.el-input {
  width: 80%;
}
.el-form-item__label {
  width: 15%;
}
.el-table-column {
  width: 100%;
}
</style>

<script>
export default {
  name: "index",
  data() {
    return {
      dialogVisible: false,
      tableData: [],
      dialogFormVisible: false,
      isEdit: false, //是否修改
      editId: "",
      delId: "",
      form: {
        id: "",
        person_name: "",
        gender: "",
        title: "",
        person_id: "",
        person_id_type: "",
        country: "",
        birth: "",
        major_id: "",
        major_name: "",
        family_address: "",
        family_zipcode: "",
        family_tel: "",
        enroll_date: "",
        email: "",
        password: ""
      },
      rules: {

      }
    };
  },

  methods: {

    sendRequest(url, opt = {}) {
      var _this = this;
      _this.$http.post(url, JSON.stringify(opt), { emulateJSON: true }).then(function(res){
          console.log(res)
          var resbody = JSON.parse(res.bodyText)
          if (url === "/api/teacher/mod") {
            if (resbody["code"] == 0) {
              _this.$message.error("修改教师信息失败：" + resbody["msg"]);
            } else {
              _this.$http.get("/api/teacher/get", {params: { id: _this.editId }}).then(function(res) {
                  console.log(res);
                  _this.tableData[_this.editIndex] = res.data["list"][0];
                  _this.getAllData()
                });
            }
          }
        })
        .catch(function(error) {
          console.log(error);
        });
    },


    submitFrom() {
      const that = this;
      this.$refs["form"].validate(valid => {
        if (valid) {
          if (that.isEdit) {
            let subForm = that.form
            delete subForm.id
            // 修改
            that.sendRequest("/api/teacher/mod", {"where":{"id":localStorage.getItem('id')},"update":subForm});
          }
          that.dialogFormVisible = false;
          // that.getAllData()
        } else {
          console.log("error submit!!");
          return false;
        }
      });
    },

    editData(index) {
      // console.log(this.tableData.teacherName)
      const selfData = this.tableData[index]
      this.editIndex = index
      this.editId = selfData.id
      this.dialogFormVisible = true
      this.isEdit = true
      this.form.id = selfData.id
      this.form.person_name = selfData.person_name
      this.form.gender = selfData.gender
      this.form.title = selfData.title
      this.form.person_id_type = selfData.person_id_type
      this.form.person_id = selfData.person_id
      this.form.country = selfData.country
      this.form.birth = selfData.birth
      this.form.major_id = selfData.major_id
      this.form.major_name = selfData.major_name
      this.form.family_address = selfData.family_address
      this.form.family_zipcode = selfData.family_zipcode
      this.form.family_tel = selfData.family_tel
      this.form.enroll_date = selfData.enroll_date
      this.form.email = selfData.email
    },

    // 请求数据
    getAllData() {
      var _this = this;
      //console.log(JSON.parse(window.localStorage.teaInfo).username)
      this.$http.get("/api/teacher/get",{params:{"id":localStorage.getItem('id')}}).then(function(res) {
          console.log(res);
          if(res.data.list.length === 0||res.data.code ==0) {
            _this.$message.error("查询教师失败")
            alert('该系统还没有您的个人信息，请联系教学管理员')
          }
          else _this.tableData = res.data["list"];
        })
        .catch(function(error) {
          console.log(error);
        });
    },

    reload() {
      this.isRouterAlive = false; //先关闭，
      this.$nextTick(function() {
        this.isRouterAlive = true; //再打开
      });
    },

    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },

    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  },

  watch: {
    dialogFormVisible() {
      if (!this.dialogFormVisible) this.isEdit = false;
    }
  },
  mounted: function() {
    // 组件创建时候去获取所有的用户数据
    this.getAllData();
  }
};
</script>

