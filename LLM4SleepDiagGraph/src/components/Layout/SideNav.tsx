/**
 * SideNav组件 - 侧边导航栏组件
 * 提供应用程序的侧边导航功能，支持左右两侧的导航栏
 */
import React from 'react';
import { SideNavigation, Tip } from '@neo4j-ndl/react';
import {
  ArrowRightIconOutline,
  ArrowLeftIconOutline,
  CloudArrowUpIconSolid,
} from '@neo4j-ndl/react/icons';
import { SideNavProps } from '../../types';
import { tooltips } from '../../utils/Constants';

/**
 * SideNav组件属性接口
 * @property {boolean} isExpanded - 导航栏是否展开
 * @property {'left' | 'right'} position - 导航栏位置
 * @property {() => void} toggleDrawer - 切换导航栏展开状态的回调函数
 */
const SideNav: React.FC<SideNavProps> = ({
  isExpanded,
  position,
  toggleDrawer,
}) => {
  /**
   * 处理导航栏点击事件
   * 切换导航栏的展开/收起状态
   */
  const handleClick = () => {
    toggleDrawer();
  };

  return (
    // 导航栏容器：设置高度和最小高度
    <div style={{ height: 'calc(100vh - 58px)', minHeight: '200px', display: 'flex' }}>
      {/* Neo4j导航组件 */}
      <SideNavigation iconMenu={true} expanded={false} position={position}>
        <SideNavigation.List>
          {/* 导航项：根据展开状态和位置显示不同的图标 */}
          <SideNavigation.Item
            onClick={handleClick}
            icon={
              isExpanded ? (
                // 展开状态：显示箭头图标
                position === 'left' ? (
                  <ArrowLeftIconOutline />
                ) : (
                  <ArrowRightIconOutline />
                )
              ) : position === 'left' ? (
                // 收起状态且为左侧导航：显示上传图标
                <>
                  <Tip allowedPlacements={['right']}>
                    <Tip.Trigger>
                      <CloudArrowUpIconSolid />
                    </Tip.Trigger>
                    <Tip.Content>{tooltips.sources}</Tip.Content>
                  </Tip>
                </>
              ) : null // 收起状态且为右侧导航：不显示图标
            }
          />
        </SideNavigation.List>
      </SideNavigation>
    </div>
  );
};

export default SideNav;
