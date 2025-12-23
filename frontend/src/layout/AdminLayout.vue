<template>
  <div>
    <el-menu mode="horizontal" router>
      <el-menu-item index="/admin">看板</el-menu-item>
      <el-menu-item index="/admin/users">用户</el-menu-item>
      <el-menu-item index="/admin/permissions">权限</el-menu-item>
      <el-menu-item index="/admin/logs">审计日志</el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>
