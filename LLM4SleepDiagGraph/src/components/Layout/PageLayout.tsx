/**
 * PageLayout组件 - 应用程序的主布局组件
 * 负责管理整体页面结构，包括侧边栏、内容区域和抽屉组件的布局
 */
import { useState } from 'react';
import SideNav from './SideNav';
import DrawerDropzone from './DrawerDropzone';
import Content from '../Content';
import SettingsModal from '../Popups/Settings/SettingModal';
import { useCredentials } from '../../context/UserCredentials';
import { UserCredentials, alertStateType } from '../../types';
import { AlertColor, AlertPropsColorOverrides } from '@mui/material';
import { OverridableStringUnion } from '@mui/types';
import { useFileContext } from '../../context/UsersFiles';
import SchemaFromTextDialog from '../Popups/Settings/SchemaFromText';
import CustomAlert from '../UI/Alert';

/**
 * PageLayoutNew组件属性接口
 * @property {boolean} isSettingPanelExpanded - 设置面板是否展开
 * @property {() => void} closeSettingModal - 关闭设置模态框的回调函数
 * @property {() => void} openSettingsDialog - 打开设置对话框的回调函数
 */
export default function PageLayoutNew({
  isSettingPanelExpanded,
  closeSettingModal,
  openSettingsDialog,
}: {
  isSettingPanelExpanded: boolean;
  closeSettingModal: () => void;
  openSettingsDialog: () => void;
}) {
  // 状态管理
  const [isLeftExpanded, setIsLeftExpanded] = useState<boolean>(true); // 左侧抽屉展开状态
  const [isRightExpanded, setIsRightExpanded] = useState<boolean>(true); // 右侧抽屉展开状态
  const [showEnhancementDialog, setshowEnhancementDialog] = useState<boolean>(false); // 增强对话框显示状态
  const { userCredentials } = useCredentials(); // 用户凭证上下文
  const toggleLeftDrawer = () => setIsLeftExpanded(!isLeftExpanded); // 切换左侧抽屉状态
  const toggleRightDrawer = () => setIsRightExpanded(!isRightExpanded); // 切换右侧抽屉状态
  
  // 警告提示状态管理
  const [alertDetails, setalertDetails] = useState<alertStateType>({
    showAlert: false,
    alertType: 'error',
    alertMessage: '',
  });
  
  // 文件上下文状态
  const { isSchema, setIsSchema, setShowTextFromSchemaDialog, showTextFromSchemaDialog } = useFileContext();

  /**
   * 显示警告提示
   * @param {string} alertmsg - 警告消息内容
   * @param {AlertColor} alerttype - 警告类型
   */
  const showAlert = (
    alertmsg: string,
    alerttype: OverridableStringUnion<AlertColor, AlertPropsColorOverrides> | undefined
  ) => {
    setalertDetails({
      showAlert: true,
      alertMessage: alertmsg,
      alertType: alerttype,
    });
  };
  
  /**
   * 关闭警告提示
   */
  const handleClose = () => {
    setalertDetails({
      showAlert: false,
      alertType: 'info',
      alertMessage: '',
    });
  };

  return (
    // 主容器：设置最大高度并启用溢出隐藏
    <div style={{ maxHeight: 'calc(100vh - 58px)' }} className='flex overflow-hidden'>
      {/* 警告提示组件 */}
      {alertDetails.showAlert && (
        <CustomAlert
          severity={alertDetails.alertType}
          open={alertDetails.showAlert}
          handleClose={handleClose}
          alertMessage={alertDetails.alertMessage}
        />
      )}
      
      {/* 左侧导航栏 */}
      <SideNav isExpanded={isLeftExpanded} position='left' toggleDrawer={toggleLeftDrawer} />
      
      {/* 左侧文件上传抽屉 */}
      <DrawerDropzone isExpanded={isLeftExpanded} />
      
      {/* 文本模式对话框 */}
      <SchemaFromTextDialog
        open={showTextFromSchemaDialog.show}
        openSettingsDialog={openSettingsDialog}
        onClose={() => {
          setShowTextFromSchemaDialog({ triggeredFrom: '', show: false });
          switch (showTextFromSchemaDialog.triggeredFrom) {
            case 'enhancementtab':
              setshowEnhancementDialog(true);
              break;
            case 'schemadialog':
              openSettingsDialog();
              break;
            default:
              break;
          }
        }}
        showAlert={showAlert}
      />
      
      {/* 设置模态框 */}
      <SettingsModal
        openTextSchema={() => {
          setShowTextFromSchemaDialog({ triggeredFrom: 'schemadialog', show: true });
        }}
        open={isSettingPanelExpanded}
        onClose={closeSettingModal}
        settingView='headerView'
        isSchema={isSchema}
        setIsSchema={setIsSchema}
      />
      
      {/* 主要内容区域 */}
      <Content
        isLeftExpanded={isLeftExpanded}
        openTextSchema={() => {
          setShowTextFromSchemaDialog({ triggeredFrom: 'schemadialog', show: true });
        }}
        isSchema={isSchema}
        setIsSchema={setIsSchema}
        showEnhancementDialog={showEnhancementDialog}
        setshowEnhancementDialog={setshowEnhancementDialog}
        closeSettingModal={closeSettingModal}
        showChatBot={false}
        openChatBot={() => {}}
      />
    </div>
  );
}