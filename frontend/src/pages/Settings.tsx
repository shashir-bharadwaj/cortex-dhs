import React from 'react';
import { Typography } from 'antd';

const { Title, Paragraph } = Typography;

const SettingsPage: React.FC = () => {
  return (
    <div>
      <Title level={3}>Settings</Title>
      <Paragraph>Here you can configure user preferences, manage roles and permissions, and customize alert rules in future versions.</Paragraph>
    </div>
  );
};

export default SettingsPage;