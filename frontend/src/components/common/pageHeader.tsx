import React from "react";
import { Typography, Button } from "antd";

const { Title } = Typography;

interface PageHeaderProps {
  title: string;
  actionLabel?: string;
  onActionClick?: () => void;
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  actionLabel,
  onActionClick,
}) => {
  return (
    <div
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 16,
      }}
    >
      <Title level={3} style={{ margin: 0 }}>
        {title}
      </Title>

      {actionLabel && onActionClick && (
        <Button danger onClick={onActionClick}>
          {actionLabel}
        </Button>
      )}
    </div>
  );
};

export default PageHeader;