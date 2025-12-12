
"use client"
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';

const TestResizable = () => {
  return (
    <div className="h-screen w-screen flex">
      <PanelGroup direction="horizontal">
        <Panel defaultSize={50} minSize={20} className="bg-blue-200 flex items-center justify-center">
          Left Panel
        </Panel>

        <PanelResizeHandle className="w-2 bg-gray-400 cursor-col-resize" />

        <Panel defaultSize={50} minSize={20} className="bg-green-200 flex items-center justify-center">
          Right Panel
        </Panel>
      </PanelGroup>
    </div>
  );
};

export default TestResizable;
