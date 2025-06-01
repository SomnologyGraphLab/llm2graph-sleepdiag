import { Drawer } from '@neo4j-ndl/react';
import Chatbot from '../ChatBot/Chatbot';
import { Messages } from '../../types';
import { useMessageContext } from '../../context/UserMessages';
import ButtonWithToolTip from '../UI/ButtonWithToolTip';
import { Flex } from '@neo4j-ndl/react';
import DeletePopUp from '../UI/DeletePopUp';

interface DrawerChatbotProps {
  isExpanded: boolean;
  clearHistoryData: boolean;
  messages: Messages[];
  selectedfileslength: number;
  setshowDeletePopUp: React.Dispatch<React.SetStateAction<boolean>>;
  tooltips: {
    deleteFile: string;
    deleteSelectedFiles: string;
    generateGraph: string;
    showGraph: string;
  };
  buttonCaptions: {
    deleteFiles: string;
    generateGraph: string;
    showPreviewGraph: string;
  };
  disableCheck: boolean;
  newFilecheck: number;
  showGraphCheck: boolean;
  completedfileNo: number;
  onClickHandler: () => void;
  handleGraphView: () => void;
  showDeletePopUp: boolean;
  deleteLoading: boolean;
  handleDeleteFiles: (delentities: boolean) => void;
}

const DrawerChatbot: React.FC<DrawerChatbotProps> = ({ isExpanded, clearHistoryData, messages, selectedfileslength, setshowDeletePopUp, tooltips, buttonCaptions, disableCheck, newFilecheck, showGraphCheck, completedfileNo, onClickHandler, handleGraphView, showDeletePopUp: externalShowDeletePopUp, deleteLoading, handleDeleteFiles }) => {
  const { setMessages } = useMessageContext();

  const getIsLoading = (messages: Messages[]) => {
    return messages.some((msg) => msg.isTyping || msg.isLoading);
  };

  return (
    <div className='flex min-h-[calc(-58px+100vh)] relative'>
      <Drawer expanded={isExpanded} closeable={false} position='right' type='push' className='!pt-0'>
        <Drawer.Body className='!overflow-hidden !pr-0'>
          <Chatbot
            isFullScreen={false}
            messages={messages}
            setMessages={setMessages}
            clear={clearHistoryData}
            isLoading={getIsLoading(messages)}
          />
          <Flex flexDirection="row" gap="4" className="self-end">
            <ButtonWithToolTip
              text={tooltips.generateGraph}
              placement="top"
              label="generate graph"
              onClick={onClickHandler}
              disabled={disableCheck}
              className="mr-0.5"
            >
              {buttonCaptions.generateGraph}
              {selectedfileslength && !disableCheck && newFilecheck ? `(${newFilecheck})` : ''}
            </ButtonWithToolTip>
            <ButtonWithToolTip
              text={tooltips.showGraph}
              placement="top"
              onClick={handleGraphView}
              disabled={showGraphCheck}
              className="mr-0.5"
              label="show graph"
            >
              {buttonCaptions.showPreviewGraph}
              {selectedfileslength && completedfileNo ? `(${completedfileNo})` : ''}
            </ButtonWithToolTip>
            <ButtonWithToolTip
              text={
                !selectedfileslength
                  ? tooltips.deleteFile
                  : `${selectedfileslength} ${tooltips.deleteSelectedFiles}`
              }
              placement="top"
              onClick={() => setshowDeletePopUp(true)}
              disabled={!selectedfileslength}
              className="ml-0.5"
              label="Delete Files"
            >
              {buttonCaptions.deleteFiles}
              {selectedfileslength !== undefined && selectedfileslength > 0 && `(${selectedfileslength})`}
            </ButtonWithToolTip>
          </Flex>
          {showDeletePopUp && (
            <DeletePopUp
              open={showDeletePopUp}
              no_of_files={selectedfileslength ?? 0}
              deleteHandler={(delentities: boolean) => handleDeleteFiles(delentities)}
              deleteCloseHandler={() => setshowDeletePopUp(false)}
              loading={deleteLoading}
              view="contentView"
            />
          )}
        </Drawer.Body>
      </Drawer>
    </div>
  );
};

export default DrawerChatbot;
